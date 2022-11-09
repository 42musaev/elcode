from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from app.users import User
from app.users.curd import UserCrudHttp
from app.users.schemas import (
    UserLoginSchema,
    UserCreateSchema,
    UserSchema,
    TokenSchema,
)
from app.users.utils import (
    create_tokens,
    update_refresh_token,
    auth
)

users = APIRouter()


@users.get("/health-check")
async def health_check(user: UserSchema = Depends(auth)):
    return user.dict() | {"status-service": "work"}


@users.post('/users', response_model=UserSchema, status_code=201)
async def create_user(user: UserCreateSchema):
    return await UserCrudHttp(User).create_user_http(user)


@users.post('/token', response_model=TokenSchema, status_code=200)
async def create_token(user: UserLoginSchema):
    user = (
        await UserCrudHttp(User).
        get_user_by_email_and_password_http(
            user.email,
            user.password,
        )
    )
    return await create_tokens(user, roles=["admin"])


@users.post('/token-refresh', status_code=200)
async def update_token(refresh_token: str):
    return await update_refresh_token(refresh_token)
