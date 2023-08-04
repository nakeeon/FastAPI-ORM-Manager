A fully typed generic manager class to easily create CRUD operations for SQLAlchemy models.

# Table of contents

1. [Quick Start](#quick-start)
    - [Manager](#manager)
    - [Searching](#searching)
2. [Pagination](#pagination)
    - [Paginator](#paginator)
    - [Pagination model](#pagination-model)

## Quick start

Assume you have an SQLAlchemy model `User`, and want to perform CRUD on this model. You can simply create a manager
for the model:

```python
from sqlalchemy_manager import Manager

from .models import User


class UserManager(Manager[User]):
    pass
```

The package also has `AsyncManager`. You can import and use it in the same way.

```python
from sqlalchemy_manager import AsynManager

from .models import User


class UserManager(AsynManager[User]):
    pass
```

`Manager` is a generic class. You need to pass an SQLAlchemy model as its type (`Manager[User]`) to configure the
manager to operate on the model.

Passing an SQLAlchemy model as the manager's type, you will also get type hints and autocompletion in your IDE.

That's it. You can now use the manager to do CRUD operations. You must initialize a manager by passing a session
instance. It should be `Session` for the `Manager` and `AsyncSession` for the `AsyncManage`.

```python
UserManager(session).create(User(firstname="Bob"))
UserManager(session).get(id=1)
UserManager(session).delete(id=1)

# Using AsyncManager
await UserManager(async_session).get(id=1)
```

### Manager

The `Manager` class contains general CRUD and extra methods such as `get_or_create` or `search`.

List of all methods:

    - get
    - create
    - delete
    - get_or_create
    - search
    - update

### Searching

The `Manager` has a `search` method. It accepts a list of SQLAlchemy expressions and simple `kwargs`.

```python
UserManager(session).search(age=10, gender="male")

UserManager(session).search(User.age >= 10)
```

## Pagination

You usually need pagination when searching. `Manager` comes with simple built-in pagination for `search` method.

The method accepts the `page` argument to return a limited set of items belonging to the page.

In `sqlalchemy_manager.pagination`, you can find `Paginator` and `Pagination` classes.

### Paginator

`Paginator` is responsible for doing the pagination and is used by the manager's `search` method.
It does an offset limit pagination under the hood and operates with `page` and `per_page` properties.
Its primary method, `paginate,` returns the `Pagination` instance.

`AsyncManager` uses `AsyncPaginator`.

`Paginator` has two properties: `per_page = 25` and `order_by = 'id'` that can be customized.

You can customize it by inheriting the `Paginator` and overriding these params in your class:

```python
from sqlalchemy_manager import Manager, Paginator


class CustomPaginator(Paginator):
    per_page = 100
    order_by = 'user_id'


class UserManager(Manager[User]):
    paginator_class = CustomPaginator
```

### Pagination model

`Pagination` is a dataclass that describes the structure of the pagination object to return.

```python
@dataclass
class Pagination:
    page: int
    results: Union[Sequence, List]
    total: int
    has_prev: bool
    has_next: bool
```
