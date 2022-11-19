import uuid
from typing import Dict

from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import insert

from app.database.conf import database
from app.notes.schemas import NoteCreateSchema
from app.notes.schemas import NoteSchema


class NoteCrud:

    def __init__(self, model):
        self.model = model

    async def create_note(self, note: NoteCreateSchema):
        query = (
            insert(self.model).
            returning(
                self.model.id,
                self.model.title,
                self.model.body,
                self.model.slug,
                self.model.created_at,
                self.model.updated_at,
            ).
            values(
                title=note.title,
                body=note.body,
                slug=uuid.uuid4().hex,
            )
        )
        return await database.fetch_one(query)


class NoteCrudHttp(NoteCrud):
    @staticmethod
    def _get_http_exception(
            status_code: int,
            detail: str, headers: Dict = None
    ) -> HTTPException:
        return HTTPException(
            status_code=status_code,
            detail=detail,
            headers=headers,
        )

    async def create_note_http(
            self,
            note: NoteCreateSchema
    ) -> NoteSchema:
        note = await self.create_note(note)
        return NoteSchema(
            id=note.id,
            title=note.title,
            body=note.body,
            slug=note.slug,
            created_at=note.created_at,
            updated_at=note.updated,
        )
