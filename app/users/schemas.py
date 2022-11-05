from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    name: str
    surname: str


class UserCreate(BaseModel):
    name: str
    surname: str
