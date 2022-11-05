from typing import List
from fastapi import APIRouter
from sqlalchemy import select, insert

from app.users import User
from app.users.schemas import UserOut, UserCreate
from app.database.conf import database

users = APIRouter()


@users.get("/users", response_model=List[UserOut])
async def get_users():
    query = select(User)
    return await database.fetch_all(query=query)


@users.post('/users', response_model=UserOut)
async def create_user(user: UserCreate):
    query = insert(User).values(user.dict())
    pk = await database.execute(query)
    return UserOut(id=pk, name=user.name, surname=user.surname)
