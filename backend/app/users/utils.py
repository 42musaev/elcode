from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt, JWTError
from starlette import status

from app.users import User

from app.users.config import Config
from app.users.curd import UserCrud
from app.users.schemas import UserSchema


async def create_tokens(user: UserSchema):
    expire = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub": user.email, "exp": expire}
    access_token = jwt.encode(
        data,
        Config.ACCESS_TOKEN_SECRET_KEY,
        algorithm=Config.ALGORITHM
    )
    expire = datetime.utcnow() + timedelta(days=Config.REFRESH_TOKEN_EXPIRE_DAYS)
    data = {"sub": user.email, "exp": expire}
    refresh_token = jwt.encode(
        data,
        Config.REFRESH_TOKEN_SECRET_KEY,
        algorithm=Config.ALGORITHM
    )
    await UserCrud(User).update_refresh_token(
        user=user,
        refresh_token=refresh_token,
        expires_token=expire
    )
    return {"access_token": access_token, "refresh_token": refresh_token}


async def update_refresh_token(token: str):
    payload = jwt.decode(token, Config.REFRESH_TOKEN_SECRET_KEY, algorithms=[Config.ALGORITHM])
    email: str = payload.get("sub")
    expire = payload.get("exp")
    user = await UserCrud(User).get_user_by_email(email=email)
    if user.refresh_token == token:
        if datetime.fromtimestamp(expire) < user.expires_token:
            return await create_tokens(user=user)
    return


async def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Config.ACCESS_TOKEN_SECRET_KEY, algorithms=[Config.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await UserCrud(User).get_user_by_email(email=email)
    if user is None:
        raise credentials_exception
    return user
