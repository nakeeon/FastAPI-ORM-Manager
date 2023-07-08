from asyncio import iscoroutinefunction
from functools import wraps

from sqlalchemy.exc import SQLAlchemyError


def catch_sqlalchemy_error(method):
    """
    A decorator to catch SQLAlchemyError for a method.
    """

    @wraps(method)
    def wrapper(cls, session, *args, **kwargs):
        try:
            return method(cls, session, *args, **kwargs)
        except SQLAlchemyError:
            session.rollback()
            raise

    @wraps(method)
    async def async_wrapper(cls, session, *args, **kwargs):
        try:
            return await method(cls, session, *args, **kwargs)
        except SQLAlchemyError:
            await session.rollback()
            raise

    if iscoroutinefunction(method):
        return async_wrapper

    return wrapper
