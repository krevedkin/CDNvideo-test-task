from sqlalchemy import delete, insert, select
from sqlalchemy.exc import IntegrityError

from src.db.db import async_session_maker
from src.models.base import BaseModel


class RecordAlreadyExistsError(Exception):
    ...


class BaseDao:
    model = None

    @classmethod
    async def get(cls, **filters) -> BaseModel | None:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            res = await session.execute(query)

            return res.scalars().first()

    @classmethod
    async def get_all(cls) -> list:
        async with async_session_maker() as session:
            query = select(cls.model)
            res = await session.execute(query)

            return res.scalars().all()

    @classmethod
    async def create(cls, **data) -> None:
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data)

            try:
                await session.execute(stmt)
                await session.commit()
            except IntegrityError:
                raise RecordAlreadyExistsError("Record already exists")

    @classmethod
    async def delete(cls, **filters) -> BaseModel | None:
        async with async_session_maker() as session:
            stmt = delete(cls.model).filter_by(**filters).returning(cls.model)

            res = await session.execute(stmt)
            await session.commit()

            return res.first()
