from datetime import datetime

from pydantic import BaseModel, validator


class NoteSchema(BaseModel):
    id: int
    title: str
    body: str
    slug: str
    created_at: int
    updated_at: int | None

    @validator(
        'created_at',
        'updated_at',
        pre=True,
    )
    def datetime_to_int(cls, value):
        if isinstance(value, datetime):
            value = int(datetime.timestamp(value))
        return value


class NoteCreateSchema(BaseModel):
    title: str
    body: str
