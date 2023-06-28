from typing import List, Sequence, Union

from pydantic import BaseModel
from sqlalchemy import func, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


class Pagination(BaseModel):
    page: int
    results: Union[Sequence[any], List[any]]
    total: int
    has_prev: bool
    has_next: bool


class Paginator:
    per_page: int = 25
    order_by: str = 'id'

    def __init__(self, model, session: Union[Session, AsyncSession], statement: Select, page: int = 1):
        self.model = model
        self.session = session
        self.statement = statement
        self.page = page

    def get_results(self) -> Sequence[any]:
        statement = self.statement.limit(self.per_page).offset((self.page - 1) * self.per_page)

        items = self.session.execute(statement)

        return items.scalars().all()

    async def async_get_results(self) -> Sequence[any]:
        statement = self.statement.limit(self.per_page).offset((self.page - 1) * self.per_page).order_by(self.order_by)

        items = await self.session.execute(statement)

        return items.scalars().all()

    def get_total(self) -> int:
        return self.session.execute(
            self.statement.with_only_columns(func.count(getattr(self.model, self.order_by)))).scalar()

    async def async_get_total(self) -> int:
        total = await self.session.execute(
            self.statement.with_only_columns(func.count(getattr(self.model, self.order_by))))

        return total.scalar()

    def has_next(self, total: int) -> bool:
        return (self.page * self.per_page) < total

    def has_prev(self) -> bool:
        return self.page > 1

    def paginate(self) -> Pagination:
        total = self.get_total()

        return Pagination(
            page=self.page,
            results=self.get_results(),
            total=self.get_total(),
            has_prev=self.has_prev(),
            has_next=self.has_next(total),
        )

    async def async_paginate(self) -> Pagination:
        results = await self.async_get_results()
        total = await self.async_get_total()

        return Pagination(
            page=self.page,
            results=results,
            total=total,
            has_prev=self.has_prev(),
            has_next=self.has_next(total),
        )
