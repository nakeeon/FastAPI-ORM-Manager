from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from .meta import SQLAlchemyErrorHandlerMeta

T = TypeVar('T')


class BaseManager(Generic[T], metaclass=SQLAlchemyErrorHandlerMeta):
    model: Type[T]

    class Params(BaseModel):
        pass

    @classmethod
    def add(cls, session: Session, instance: T):
        session.add(instance)
        session.commit()

    @classmethod
    async def async_add(cls, session: AsyncSession, instance: T):
        session.add(instance)
        await session.commit()

    @classmethod
    def get(cls, session: Session, **kwargs) -> T:
        statement = select(cls.model).filter_by(**kwargs)

        item = session.execute(statement)

        try:
            return item.scalar()
        except NoResultFound:
            return None

    @classmethod
    async def async_get(cls, session: AsyncSession, **kwargs) -> T:
        statement = select(cls.model).filter_by(**kwargs)
        item = await session.execute(statement)

        try:
            return item.scalar()
        except NoResultFound:
            return None

    @classmethod
    def search(cls, session: Session, params: Params) -> [T]:
        statement = select(cls.model).filter_by(**params.dict(exclude_none=True))

        items = session.execute(statement)
        return items.scalars().all()

    @classmethod
    async def async_search(cls, session: AsyncSession, params: Params) -> [T]:
        statement = select(cls.model).filter_by(**params.dict(exclude_none=True))

        items = await session.execute(statement)
        return items.scalars().all()

    @classmethod
    def update(cls, session: Session, instance: T, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        session.commit()

    @classmethod
    async def async_update(cls, session: AsyncSession, instance: T, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)

        await session.commit()

    @classmethod
    def delete(cls, session: Session, instance: T):
        session.delete(instance)
        session.commit()

    @classmethod
    async def async_delete(cls, session: AsyncSession, instance: T):
        await session.delete(instance)
        await session.commit()
