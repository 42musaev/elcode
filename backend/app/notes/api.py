from fastapi import APIRouter
from fastapi import Depends

from app.notes.crud import NoteCrudHttp
from app.users.schemas import UserSchema
from app.users.utils import auth

from app.notes.schemas import NoteSchema
from app.notes.schemas import NoteCreateSchema
from app.notes.models import Note

notes = APIRouter(prefix='/notes', tags=['notes'])


@notes.get("/health-check")
async def health_check(user: UserSchema = Depends(auth)):
    return user.dict() | {"status-service": "work"}


@notes.post('', status_code=201, response_model=NoteSchema)
async def create_note(note: NoteCreateSchema):
    return await NoteCrudHttp(Note).create_note_http(note)
