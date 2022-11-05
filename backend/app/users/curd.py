from typing import Dict
from fastapi import HTTPException
from sqlalchemy import insert, select
from starlette import status
from app.database.conf import database
from app.users.schemas import UserSchema, UserCreateSchema
from app.users.utils import get_password_hash


class UserCrud:

    def __init__(self, model):
        self.model = model

    async def create_user(self, data_user: UserCreateSchema) -> UserSchema | Dict:
        user = await self.get_user_by_email(data_user.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail={"detail": "email already exists"}
            )
        query = insert(self.model).values(
            email=data_user.email,
            hashed_password=get_password_hash(data_user.password.get_secret_value()),
            disable=data_user.disable,
        )
        pk = await database.execute(query)
        return UserSchema(id=pk, email=data_user.email)

    async def get_user_by_email(self, email):
        query = select(self.model).where(self.model.email == email)
        user = await database.fetch_one(query)
        if user:
            return UserSchema(**user)
