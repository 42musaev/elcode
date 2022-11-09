from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from app.users import User
from app.users.curd import UserCrud
from app.users.schemas import (
    UserLoginSchema,
    UserCreateSchema,
    UserSchema,
    TokenSchema, RefreshToken,
)
from app.users.utils import create_tokens, update_refresh_token, get_current_user

users = APIRouter()


@users.get('/ping')
async def ping(user: UserSchema = Depends(get_current_user)):
    return UserSchema(user.dict())

@users.post('/token', response_model=TokenSchema, status_code=200)
async def create_token(user: UserLoginSchema):
    user = await UserCrud(User).get_user_by_email_and_password(
        user.email,
        user.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await create_tokens(user)


@users.post('/token-refresh')
async def update_token(refresh_token: str):
    updated = await update_refresh_token(refresh_token)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return updated


@users.post('/users', response_model=UserSchema, status_code=201)
async def create_user(user: UserCreateSchema):
    return await UserCrud(User).create_user(user)
