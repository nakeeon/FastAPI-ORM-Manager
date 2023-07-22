from typing import List, Sequence, Union

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

try:
    from pydantic.dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass


@dataclass
class Pagination:
    page: int
    items: Union[Sequence, List]
    total: int
    has_prev: bool
    has_next: bool


class BasePaginator:
    per_page: int = 25
    order_by: str = 'id'

    def __init__(self, model, session: Union[Session, AsyncSession], statement, page: int = 1):
        self.model = model
        self.session = session
        self.statement = statement
        self.page = page

    def _get_paginated_statement(self):
        return self.statement.limit(self.per_page).offset((self.page - 1) * self.per_page).order_by(self.order_by)

    def _get_total_statement(self):
        return self.statement.with_only_columns(func.count(getattr(self.model, self.order_by)))

    def has_next(self, total: int) -> bool:
        return (self.page * self.per_page) < total

    def has_prev(self) -> bool:
        return self.page > 1


class Paginator(BasePaginator):
    def get_items(self) -> Sequence[any]:
        items = self.session.execute(self._get_paginated_statement())

        return items.scalars().all()

    def get_total(self) -> int:
        return self.session.execute(self._get_total_statement()).scalar()

    def paginate(self) -> Pagination:
        total = self.get_total()

        return Pagination(
            page=self.page,
            items=self.get_items(),
            total=self.get_total(),
            has_prev=self.has_prev(),
            has_next=self.has_next(total),
        )


class AsyncPaginator(BasePaginator):

    async def get_items(self) -> Sequence[any]:
        items = await self.session.execute(self._get_paginated_statement())

        return items.scalars().all()

    async def get_total(self) -> int:
        total = await self.session.execute(self._get_total_statement())

        return total.scalar()

    async def paginate(self) -> Pagination:
        items = await self.get_items()
        total = await self.get_total()

        return Pagination(
            page=self.page,
            items=items,
            total=total,
            has_prev=self.has_prev(),
            has_next=self.has_next(total),
        )
