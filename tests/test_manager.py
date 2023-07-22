from tests import User, UserScheme


def test_create(test_db, user_manager):
    user_name = 'Bob'

    user_manager.create(test_db, User(name=user_name))
    user = user_manager.get(test_db, name=user_name)

    assert user is not None
    assert user.name == user_name


def test_create_pydantic(test_db, user_manager):
    user_name = 'Bob'
    user_manager.create(test_db, UserScheme(id=1, name=user_name))
    user = user_manager.get(test_db, name=user_name)

    assert user is not None
    assert user.name == user_name


def test_get(test_db, user_manager):
    user_name = 'Bob'

    user_manager.create(test_db, User(name=user_name))
    user = user_manager.get(test_db, name=user_name)

    assert user is not None
    assert user.name == user_name

    # get not existing user
    user = user_manager.get(test_db, name='nothing')

    assert user is None


def test_update(test_db, user_manager):
    # create a user first
    user = user_manager.create(test_db, User(name='Bob', lastname='Johnson'))
    # update name
    user_manager.update(test_db, user, name='Carl', lastname='Carlson')
    # get by new name
    user = user_manager.get(test_db, name='Carl', lastname='Carlson')

    assert user is not None


def test_delete(test_db, user_manager):
    # create first
    user = user_manager.create(test_db, User(name='Bob'))

    user_manager.delete(test_db, user)
    user = user_manager.get(test_db, name='Bob')

    assert user is None


def test_get_or_create(test_db, user_manager):
    # create
    user, created = user_manager.get_or_create(test_db, name='Bob', lastname='Johnson')

    assert user is not None
    assert created

    # get existing
    user, created = user_manager.get_or_create(test_db, name='Bob', lastname='Johnson')

    assert user is not None
    assert not created


def test_search(test_db, user_manager):
    user_manager.create(test_db, User(name='Bob', lastname='Johnson'))
    user_manager.create(test_db, User(name='Bob', lastname='Carlson'))

    result = user_manager.search(test_db, {'name': 'Bob', 'lastname': None})

    assert result.total == 2

    result = user_manager.search(test_db, user_manager.Params(name='Bob'))

    assert result.total == 2
