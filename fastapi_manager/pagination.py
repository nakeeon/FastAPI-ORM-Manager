from typing import Sequence, Union

from pydantic import BaseModel
from sqlalchemy import func, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


class Pagination(BaseModel):
    page: int
    results: Sequence
    total: int
    has_prev: bool
    has_next: bool


class Paginator:
    per_page = 25

    def __init__(self, session: Union[Session, AsyncSession], statement: Select, page: int = 1):
        self.session = session
        self.statement = statement
        self.page = page

    def get_results(self) -> Sequence[any]:
        statement = self.statement.limit(self.per_page).offset((self.page - 1) * self.per_page)

        items = self.session.execute(statement)

        return items.scalars().all()

    async def async_get_results(self) -> Sequence[any]:
        statement = self.statement.limit(self.per_page).offset((self.page - 1) * self.per_page)

        items = await self.session.execute(statement)

        return items.scalars().all()

    def get_total(self) -> int:
        return self.session.execute(self.statement.with_only_columns(func.count())).scalar()

    async def async_get_total(self) -> int:
        total = await self.session.execute(self.statement.with_only_columns(func.count()))

        return total.scalar()

    def has_next(self) -> bool:
        return (self.page * self.per_page) < self.get_total()

    async def async_has_next(self) -> bool:
        total = await self.async_get_total()

        return (self.page * self.per_page) < total

    def has_prev(self) -> bool:
        return self.page > 1

    def paginate(self) -> Pagination:
        return Pagination(
            page=self.page,
            results=self.get_results(),
            total=self.get_total(),
            has_prev=self.has_prev(),
            has_next=self.has_next(),
        )

    async def async_paginate(self) -> Pagination:
        results = await self.async_get_results()
        total = await self.async_get_total()
        has_next = await self.async_has_next()

        return Pagination(
            page=self.page,
            results=results,
            total=total,
            has_prev=has_next,
            has_next=self.has_next(),
        )
