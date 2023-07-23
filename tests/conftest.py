import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy_manager import AsyncManager, Manager
from tests import Base, User


@pytest.fixture(scope='function')
def test_db():
    engine = create_engine('sqlite:///:memory:')  # Use an in-memory SQLite database for tests
    testing_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create all tables
    Base.metadata.create_all(engine)

    # Use the session in our tests
    session = testing_session()

    yield session

    # After tests are done, tear down the session and drop all tables
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
async def async_session():
    database_url = 'sqlite+aiosqlite:///:memory:'
    engine = create_async_engine(database_url)
    Session = async_sessionmaker(engine)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session = Session()
    return session


@pytest.fixture(scope="function")
def user_manager(test_db):
    class UserManager(Manager[User]):
        pass

    return UserManager(test_db)


@pytest.fixture(scope="function")
async def get_async_user_manager(async_session):
    session = await async_session

    class UserManager(AsyncManager[User]):
        pass

    return UserManager(session)
