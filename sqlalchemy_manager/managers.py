from typing import Any, Generic, Tuple, Type, TypeVar, Union

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from .meta import ManagerMeta
from .pagination import AsyncPaginator, Pagination, Paginator

T = TypeVar('T')


class BaseManager(Generic[T], metaclass=ManagerMeta):
    model: Type[T]

    def __init__(self, session: Union[Session, AsyncSession]):
        self.session = session


class AsyncManager(BaseManager, Generic[T]):
    paginator_class = AsyncPaginator

    async def create(self, instance: T, commit: bool = True) -> T:
        self.session.add(instance)

        if commit:
            await self.session.commit()

        return instance

    async def get(self, **kwargs) -> Union[T, None]:
        statement = select(self.model).filter_by(**kwargs)
        item = await self.session.execute(statement)

        try:
            return item.scalar()
        except NoResultFound:
            return None

    async def get_or_create(self, **kwargs) -> Tuple[T, bool]:
        commit = kwargs.get('commit', True)
        created = False
        instance = await self.get(**kwargs)

        if not instance:
            instance = self.model(**kwargs)
            await self.create(instance, commit)
            created = True

        return instance, created

    async def search(self, *criteria: Any, **params: dict) -> Pagination:
        page = params.pop('page', 1)
        statement = select(self.model)

        if params:
            statement = statement.filter_by(**params)

        if criteria:
            statement = statement.where(*criteria)

        pagination = await self.paginator_class(self.model, self.session, statement, page).paginate()

        return pagination

    async def update(self, instance: T, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)

        await self.session.commit()

    async def delete(self, instance: T):
        await self.session.delete(instance)
        await self.session.commit()


class Manager(BaseManager, Generic[T]):
    paginator_class = Paginator

    def create(self, instance: Union[T, dict], commit: bool = True) -> T:
        if isinstance(instance, dict):
            instance = self.model(**instance)

        self.session.add(instance)

        if commit:
            self.session.commit()

        return instance

    def get(self, **kwargs) -> Union[T, None]:
        item = self.session.query(self.model).filter_by(**kwargs)

        try:
            return item.scalar()
        except NoResultFound:
            return None

    def get_or_create(self, **kwargs) -> Tuple[T, bool]:
        commit = kwargs.get('commit', True)
        created = False
        instance = self.get(**kwargs)

        if not instance:
            instance = self.model(**kwargs)
            self.create(instance, commit)
            created = True

        return instance, created

    def search(self, *criteria: Any, **params: dict) -> Pagination:
        page = params.pop('page', 1)
        statement = select(self.model)

        if params:
            statement = statement.filter_by(**params)

        if criteria:
            statement = statement.where(*criteria)

        return self.paginator_class(self.model, self.session, statement, page).paginate()

    def update(self, instance: T, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)

        self.session.commit()

    def delete(self, instance: T):
        self.session.delete(instance)
        self.session.commit()
