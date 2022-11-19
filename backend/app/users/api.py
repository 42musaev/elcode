from fastapi import APIRouter
from fastapi import Depends

from app.users import User
from app.users.curd import UserCrudHttp
from app.users.schemas import UserLoginSchema
from app.users.schemas import UserCreateSchema
from app.users.schemas import UserSchema
from app.users.schemas import TokenSchema
from app.users.utils import create_tokens
from app.users.utils import update_refresh_token
from app.users.utils import auth

users = APIRouter(prefix='/users', tags=['users'])


@users.get("/health-check")
async def health_check(user: UserSchema = Depends(auth)):
    return user.dict() | {"status-service": "work"}


@users.post('', response_model=UserSchema, status_code=201)
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
