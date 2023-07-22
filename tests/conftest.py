import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy_manager import Manager
from tests import Base, User

try:
    from pydantic import BaseModel
except ImportError:
    BaseModel = object


@pytest.fixture(scope='function')
def test_db():
    engine = create_engine('sqlite:///:memory:')  # Use an in-memory SQLite database for tests
    testing_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create all tables
    Base.metadata.create_all(engine)

    # Use the session in our tests
    session = testing_session()

    yield session  # this is where the testing happens!

    # After tests are done, tear down the session and drop all tables
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def user_manager(test_db):
    class UserManager(Manager[User]):
        pass

    return UserManager(test_db)
