from asyncio import iscoroutinefunction
from functools import wraps

from sqlalchemy.exc import SQLAlchemyError


def catch_sqlalchemy_error(method):
    """
    A decorator to catch SQLAlchemyError for a method.
    """

    @wraps(method)
    async def wrapper(cls, session, *args, **kwargs):
        try:
            if iscoroutinefunction(method):
                return await method(cls, session, *args, **kwargs)
            else:
                return method(cls, session, *args, **kwargs)
        except SQLAlchemyError as e:
            if iscoroutinefunction(method):
                await session.rollback()
            else:
                session.rollback()
            raise e

    return wrapper
