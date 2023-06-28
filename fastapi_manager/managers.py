from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from .meta import ManagerMeta
from .pagination import Pagination, Paginator

T = TypeVar('T')


class Manager(Generic[T], metaclass=ManagerMeta):
    model: Type[T]
    paginator_class = Paginator

    class Params(BaseModel):
        """ A reserved pydantic model to use in filter_by expression """
        pass

    @classmethod
    def create(cls, session: Session, instance: T):
        if isinstance(instance, BaseModel):
            instance = cls.model(**instance.dict())

        session.add(instance)
        session.commit()

    @classmethod
    async def async_create(cls, session: AsyncSession, instance: T):
        if isinstance(instance, BaseModel):
            instance = cls.model(**instance.dict())

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
    def get_or_create(cls, session: Session, **kwargs) -> T:
        instance = cls.get(session, **kwargs)

        if not instance:
            instance = cls.model(**kwargs)
            cls.create(session, instance)

        return instance

    @classmethod
    async def async_get_or_create(cls, session: AsyncSession, **kwargs) -> T:
        instance = await cls.async_get(session, **kwargs)

        if not instance:
            instance = cls.model(**kwargs)
            await cls.async_create(session, instance)

        return instance

    @classmethod
    def search(cls, session: Session, params: Params, page: int = 1) -> Pagination:
        statement = select(cls.model).filter_by(**params.dict(exclude_none=True))

        return cls.paginator_class(cls.model, session, statement, page).paginate()

    @classmethod
    async def async_search(cls, session: AsyncSession, params: Params, page: int = 1) -> Pagination:
        statement = select(cls.model).filter_by(**params.dict(exclude_none=True))

        pagination = await cls.paginator_class(cls.model, session, statement, page).async_paginate()

        return pagination

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
