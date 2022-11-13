from datetime import datetime
from datetime import timedelta
from typing import List

from jose import jwt
from jose import JWTError

from starlette import status
from starlette.requests import Request

from app.users import User
from app.users.curd import UserCrud
from app.users.curd import UserCrudHttp
from app.users.schemas import UserSchema
from app.config import get_settings

from fastapi.security import HTTPBearer
from fastapi import HTTPException

settings = get_settings()


class OptionalHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> UserSchema | HTTPException:
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


async def create_tokens(
        user: UserSchema,
        roles: List[str] = None,
):
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    data = {"sub": user.email, "exp": expire, "roles": roles}
    access_token = jwt.encode(
        data,
        settings.ACCESS_TOKEN_SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    expire = datetime.utcnow() + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    data = {"sub": user.email, "exp": expire}
    refresh_token = jwt.encode(
        data,
        settings.REFRESH_TOKEN_SECRET_KEY,
        algorithm=settings.ALGORITHM
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
            settings.REFRESH_TOKEN_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
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
            settings.ACCESS_TOKEN_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
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
