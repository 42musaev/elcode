from asyncpg import UniqueViolationError
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from fastapi import HTTPException
from fastapi import status

from app.database.conf import database


class BaseCrud:
    model = None

    @classmethod
    async def create_object(cls, **data):
        query = insert(cls.model).values(**data)
        pk = await database.execute(query)
        return await cls.get_one_or_none(id=pk)

    @classmethod
    async def get_one_or_none(cls, **filter_args):
        query = select(cls.model).filter_by(**filter_args)
        return await database.fetch_one(query)

    @classmethod
    async def update_object(cls, pk, **data):
        query = update(cls.model).where(cls.model.id == pk).values(**data)
        return await database.fetch_one(query)

    @classmethod
    async def http_create_object(cls, **data):
        try:
            return await cls.create_object(**data)
        except UniqueViolationError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{cls.model.__name__} already exists"
            )
