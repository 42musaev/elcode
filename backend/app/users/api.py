from datetime import timedelta

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, insert

from app.database.conf import database
from app.users import User
from app.users.schemas import UserSchema, Token, UserCreateSchema
from app.users.utils import (
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    get_current_active_user, get_password_hash
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


@users.post("/users")
async def user_create(user: UserCreateSchema):
    query = insert(User).values(email=user.email, hashed_password=get_password_hash(user.password.get_secret_value()),
                                disable=user.disable)
    pk = await database.execute(query)
    return pk
