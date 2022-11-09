from pydantic import BaseModel, EmailStr


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserCreateSchema(UserLoginSchema):
    pass


class UserSchema(BaseModel):
    id: int
    email: EmailStr


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class RefreshToken(BaseModel):
    refresh_token: str
