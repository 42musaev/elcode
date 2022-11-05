from datetime import timedelta
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from app.users import User
from app.users.curd import UserCrud
from app.users.schemas import UserSchema, Token, UserCreateSchema
from app.users.utils import (
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    get_current_active_user,
)

users = APIRouter()


@users.get("/users/ping")
async def read_own_items(current_user: UserSchema = Depends(get_current_active_user)):
    return {"ping": "pong"}


@users.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@users.post("/users", response_model=UserSchema, status_code=201)
async def user_create(user: UserCreateSchema):
    return await UserCrud(model=User).create_user(user)
