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

    result = user_manager.search({'name': 'Bob'})

    assert result.total == 2

    result = user_manager.search({'lastname': 'Carlson'})

    assert result.total == 1
