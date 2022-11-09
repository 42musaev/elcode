from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import HTTPException
from jose import jwt, JWTError
from starlette import status
from starlette.requests import Request
from app.users import User
from app.users.config import Config
from fastapi.security import HTTPBearer

from app.users.curd import UserCrud, UserCrudHttp
from app.users.schemas import UserSchema


class OptionalHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        from fastapi import status
        try:
            r = await super().__call__(request)
            token = r.credentials
        except HTTPException as ex:
            assert ex.status_code == status.HTTP_403_FORBIDDEN, ex
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return await get_current_user(token)


auth = OptionalHTTPBearer()


async def create_tokens(user: UserSchema, roles: List[str] = None):
    expire = datetime.utcnow() + timedelta(
        minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    data = {"sub": user.email, "exp": expire, "roles": roles}
    access_token = jwt.encode(
        data,
        Config.ACCESS_TOKEN_SECRET_KEY,
        algorithm=Config.ALGORITHM
    )
    expire = datetime.utcnow() + timedelta(
        days=Config.REFRESH_TOKEN_EXPIRE_DAYS
    )
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
    credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            Config.REFRESH_TOKEN_SECRET_KEY,
            algorithms=[Config.ALGORITHM]
        )
    except JWTError:
        raise credentials
    email: str = payload.get("sub")
    expire = payload.get("exp")
    user = await UserCrud(User).get_user_by_email(email=email)
    if user.refresh_token == token:
        if datetime.fromtimestamp(expire) < user.expires_token:
            return await create_tokens(user=user)
    raise credentials


async def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            Config.ACCESS_TOKEN_SECRET_KEY,
            algorithms=[Config.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await (
        UserCrudHttp(User).
        get_user_by_email_http(email=email)
    )
    if user is None:
        raise credentials_exception
    return user
