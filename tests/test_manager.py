import pytest
from sqlalchemy import and_

from tests import User


def test_create(user_manager):
    user_name = 'Bob'

    user_manager.create(User(name=user_name))
    user = user_manager.get(name=user_name)

    assert user is not None
    assert user.name == user_name


def test_get(user_manager):
    user_name = 'Bob'

    user_manager.create(User(name=user_name))
    user = user_manager.get(name=user_name)

    assert user is not None
    assert user.name == user_name

    # get not existing user
    user = user_manager.get(name='nothing')

    assert user is None


def test_update(user_manager):
    # create a user first
    user = user_manager.create(User(name='Bob', lastname='Johnson'))
    # update name
    user_manager.update(user, name='Carl', lastname='Carlson')
    # get by new name
    user = user_manager.get(name='Carl', lastname='Carlson')

    assert user is not None


def test_delete(user_manager):
    # create first
    user = user_manager.create(User(name='Bob'))

    user_manager.delete(user)
    user = user_manager.get(name='Bob')

    assert user is None


def test_get_or_create(user_manager):
    # create
    user, created = user_manager.get_or_create(name='Bob', lastname='Johnson')

    assert user is not None
    assert created

    # get existing
    user, created = user_manager.get_or_create(name='Bob', lastname='Johnson')

    assert user is not None
    assert not created


def test_search(user_manager):
    user_manager.create(User(name='Bob', lastname='Johnson'))
    user_manager.create(User(name='Bob', lastname='Carlson'))

    result = user_manager.search(name='Bob')

    assert result.total == 2

    result = user_manager.search(lastname='Carlson')

    assert result.total == 1

    result = user_manager.search(name='Bob', lastname='Johnson')

    assert result.total == 1

    result = user_manager.search(and_(User.name == 'Bob', User.lastname == 'Johnson'))

    assert result.total == 1


@pytest.mark.asyncio
async def test_async_create(get_async_user_manager):
    user_manager = await get_async_user_manager
    user_name = 'Bob'

    await user_manager.create(User(name=user_name))
    user = await user_manager.get(name=user_name)

    assert user is not None
    assert user.name == user_name

    await user_manager.session.close()


@pytest.mark.asyncio
async def test_async_get(get_async_user_manager):
    user_manager = await get_async_user_manager
    user_name = 'Bob'

    await user_manager.create(User(name=user_name))
    user = await user_manager.get(name=user_name)

    assert user is not None
    assert user.name == user_name

    # get not existing user
    user = await user_manager.get(name='nothing')

    assert user is None


@pytest.mark.asyncio
async def test_async_update(get_async_user_manager):
    user_manager = await get_async_user_manager
    # create a user first
    user = await user_manager.create(User(name='Bob', lastname='Johnson'))
    # update name
    await user_manager.update(user, name='Carl', lastname='Carlson')
    # get by new name
    user = await user_manager.get(name='Carl', lastname='Carlson')

    assert user is not None


@pytest.mark.asyncio
async def test_async_delete(get_async_user_manager):
    user_manager = await get_async_user_manager
    # create first
    user = await user_manager.create(User(name='Bob'))

    await user_manager.delete(user)
    user = await user_manager.get(name='Bob')

    assert user is None


@pytest.mark.asyncio
async def test_async_get_or_create(get_async_user_manager):
    user_manager = await get_async_user_manager
    # create
    user, created = await user_manager.get_or_create(name='Bob', lastname='Johnson')

    assert user is not None
    assert created

    # get existing
    user, created = await user_manager.get_or_create(name='Bob', lastname='Johnson')

    assert user is not None
    assert not created


@pytest.mark.asyncio
async def test_async_search(get_async_user_manager):
    user_manager = await get_async_user_manager

    await user_manager.create(User(name='Bob', lastname='Johnson'))
    await user_manager.create(User(name='Bob', lastname='Carlson'))

    result = await user_manager.search(name='Bob')

    assert result.total == 2

    result = await user_manager.search(lastname='Carlson')

    assert result.total == 1

    result = await user_manager.search(name='Bob', lastname='Johnson')

    assert result.total == 1

    result = await user_manager.search(and_(User.name == 'Bob', User.lastname == 'Johnson'))

    assert result.total == 1

    await user_manager.session.close()
