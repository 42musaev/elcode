from fastapi import APIRouter
from fastapi import Depends

from app.users.schemas import UserSchema
from app.users.utils import auth

notes = APIRouter(prefix='/notes', tags=['notes'])


@notes.get("/health-check")
async def health_check(user: UserSchema = Depends(auth)):
    return user.dict() | {"status-service": "work"}
