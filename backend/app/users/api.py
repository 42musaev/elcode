
from fastapi import APIRouter
from fastapi import Depends

from app.base.schemas import HealthCheckSchema
from app.users.curd import UserCrud
from app.users.schemas import UserLoginSchema
from app.users.schemas import UserCreateSchema
from app.users.schemas import UserSchema
from app.users.schemas import TokenSchema
from app.users.utils import create_tokens
from app.users.utils import update_refresh_token
from app.users.utils import auth

users = APIRouter(prefix='/users', tags=['users'])


@users.get("/health-check")
async def health_check(user: UserSchema = Depends(auth)) -> HealthCheckSchema:
    return HealthCheckSchema(email=user.email, status_service='works')


@users.post('', status_code=201)
async def create_user(user: UserCreateSchema) -> UserSchema:
    return await UserCrud.http_create_object(
        email=user.email,
        hashed_password=user.password
    )


@users.post('/token', response_model=TokenSchema, status_code=200)
async def create_token(user: UserLoginSchema):
    user = await UserCrud.get_one_or_none(email=user.email)
    return await create_tokens(user, roles=["admin"])


@users.post('/token-refresh', status_code=200)
async def update_token(refresh_token: str):
    return await update_refresh_token(refresh_token)
