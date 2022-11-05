from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field, EmailStr, SecretStr, validator

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserSchema(BaseModel):
    id: int
    email: EmailStr


class UserCheckSchema(BaseModel):
    email: EmailStr
    hashed_password: str
    disable: bool = False


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    disable: bool = False

    @validator('password', pre=True)
    def passwords_match(cls, value):
        if len(value) < 8:
            raise ValueError('!')
        return value
