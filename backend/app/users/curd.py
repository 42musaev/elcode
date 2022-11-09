import uuid
from datetime import datetime

from sqlalchemy import insert, select, update
from app.database.conf import database
from app.users.schemas import UserSchema, UserCreateSchema
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCrud:

    def __init__(self, model):
        self.model = model

    async def create_user(self, user: UserCreateSchema):
        salt = uuid.uuid4().hex
        query = insert(self.model).values(
            email=user.email,
            hashed_password=self.password_hash(user.password)

        )
        pk = await database.execute(query)
        return UserSchema(id=pk, email=user.email)

    async def get_user_by_email(self, email):
        query = select(self.model).where(self.model.email == email)
        user = await database.fetch_one(query=query)
        return user

    async def get_user_by_email_and_password(self, email: str, password: str):
        query = select(self.model).where(self.model.email == email)
        user = await database.fetch_one(query=query)
        verify = self.verify_password(password, user.hashed_password)
        if verify:
            return UserSchema(**user)

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
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def password_hash(password):
        return pwd_context.hash(password)
