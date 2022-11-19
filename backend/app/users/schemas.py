from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
from pydantic import validator


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(default="password")


class UserCreateSchema(UserLoginSchema):
    @validator('password', always=True)
    def validate_password1(cls, value):
        min_length = 8
        errors = ''
        if len(value) < min_length:
            errors += 'Password must be at least 8 characters long. '
        if errors:
            raise ValueError(errors)
        return value


class UserSchema(BaseModel):
    id: int
    email: EmailStr


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class RefreshToken(BaseModel):
    refresh_token: str
