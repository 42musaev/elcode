from datetime import datetime
from typing import Dict

from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update

from fastapi import HTTPException
from fastapi import status

from app.database.conf import database
from app.users.schemas import UserSchema, UserCreateSchema

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCrud:

    def __init__(self, model):
        self.model = model

    async def create_user(self, user: UserCreateSchema):
        query = (
            insert(self.model).
            returning(
                self.model.id,
                self.model.email).
            values(
                email=user.email,
                hashed_password=self.password_hash(user.password)
            )
        )
        return await database.fetch_all(query)

    async def get_user_by_email(self, email):
        query = select(self.model).where(self.model.email == email)
        user = await database.fetch_one(query=query)
        if user:
            return user

    async def get_user_by_email_and_password(self, email: str, password: str):
        query = select(self.model).where(self.model.email == email)
        user = await database.fetch_one(query=query)
        if user:
            verify = self.verify_password(password, user.hashed_password)
            if verify:
                return user

    async def update_refresh_token(
            self,
            user: UserSchema,
            refresh_token: str,
            expires_token: datetime
    ):
        query = (
            update(self.model).
            where(self.model.email == user.email).
            values(refresh_token=refresh_token, expires_token=expires_token)
        )
        return await database.execute(query)

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def password_hash(password):
        return pwd_context.hash(password)


class UserCrudHttp(UserCrud):
    @staticmethod
    def _get_http_exception(
            status_code: int,
            detail: str, headers: Dict = None
    ) -> HTTPException:
        return HTTPException(
            status_code=status_code,
            detail=detail,
            headers=headers,
        )

    async def create_user_http(
            self,
            user: UserCreateSchema
    ) -> UserSchema | HTTPException:
        user_db = await self.get_user_by_email(user.email)
        if not user_db:
            user = (await self.create_user(user))[0]
            return UserSchema(
                id=user.id,
                email=user.email,
            )
        raise self._get_http_exception(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{self.model.__name__} Already exists",
        )

    async def get_user_by_email_and_password_http(
            self,
            email: str,
            password: str
    ) -> UserSchema:
        user = await self.get_user_by_email_and_password(email, password)
        if not user:
            raise self._get_http_exception(
                status.HTTP_401_UNAUTHORIZED,
                "Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return UserSchema(id=user.id, email=user.email)

    async def get_user_by_email_http(
            self,
            email: str
    ) -> UserSchema | HTTPException:
        user = await self.get_user_by_email(email)
        if not user:
            raise self._get_http_exception(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found"
            )
        return UserSchema(id=user.id, email=user.email)
