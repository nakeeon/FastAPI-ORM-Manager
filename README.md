A fully typed generic manager class to easily create CRUD operations for SQLAlchemy models. Designed to use in FastAPI
projects.

# Table of content

1. [Quick start](#quick-start)
    - [Manager](#manager)
    - [Searching](#searching)
2. [Pagination](#pagination)
    - [Paginator](#paginator)
    - [Pagination model](#pagination-model)

## Quick start

Assume you have an SQLAlchemy model `User` and you want to perform CRUD on this model. You can simply create a manager
for the model like this:

```python
from sqlalchemy_manager import Manager

from .models import User


class UserManager(Manager[User]):
    pass
```

`Manager` is a generic class, you need to pass an SQLAlchemy model as it's type (`Manager[User]`) to configure the
manager to operate the model.

By passing an SQLAlchemy model as manager's type you will also get type hints and autocompletion in your IDE.

That's it. You can now use the manager to do CRUD operations. You need to pass an SQlAlchemy session to a method as
first argument. It can be `Session` or `AsyncSession`.

```python
UserManager.create(session, User(firstname="Bob"))
UserManager.get(session, id=1)
UserManager.delete(session, id=1)
```

### Manager

`Manager` class contains general CRUD methods alongside some extra methods such as `get_or_create` and `search`.

List of all methods:

    - get
    - create
    - delete
    - get_or_create
    - search
    - update

It is also has async methods, simple add `async_` to a method name, e.g. `async_create`, `async_delete` etc.

`Manager` can accept either an SQLAlchemy model instance or a pydantic model instance.

```python
from sqlalchemy_manager import Manager
from pydantic import BaseModel

from app.db import session
from app.managers import UserManager


class User(BaseModel):
    firstname: str


user = User(firstname="Bob")
UserManager.create(session, user)  # ok
```

### Searching

Manager has `search` and `async_search` methods. It accepts search params as a pydantic model called `Params`. Each
manager has its own search params model defined inside the class.

```python
from sqlalchemy_manager import Manager
from pydantic import BaseModel

from .models import User


class UserManager(Manager[User]):
    class Params(BaseModel):
        age: int
        gender: str
```

Now `search` and `async_search` of `UserManager` will accept only `age` and `gender` params by validating them using
the `Params`
model.

You can pass either a `dict` or manager's `Params` object.

```python
UserManager.search(session, **{'age': 10, 'gender': 'male'})  # okay
UserManager.search(session, UserManager.Params(age=10, gender='male'))  # okay

UserManager.search(session, **{'age': 10, 'name': 'Bob'})  # validation error
```

## Pagination

You usually need a pagination when do search. `Manager` comes with simple builtin pagination for `search`
and `async_search` methods.

These methods accept `page` argument to return a limited set of items belonging to the page.

In `fastapi_manager.pagination` you can find `Paginator` and `Pagination` classes.

### Paginator

`Paginator` is responsible for doing the pagination and is used by manager's `search` and `async_search` methods.
It does an offset limit pagination under the hood, and operates with `page` and `per_page` properties.
Its main method `paginate` returns `Pagination` object which tells the structure of the pagination.

It has two properties: `per_page = 25` and `order_by = 'id'` that can be customized.

You can customize it by inherit the `Paginator` and override these params in your own class:

```python
from sqlalchemy_manager import Manager, Paginator


class CustomPaginator(Paginator):
    per_page = 100
    order_by = 'user_id'


class UserManager(Manager[User]):
    paginator_class = CustomPaginator
```

### Pagination model

`Pagination` is a pydantic model that describes the structure of the pagination object to be returned.

```python
class Pagination(BaseModel):
    page: int
    results: Union[Sequence, List]
    total: int
    has_prev: bool
    has_next: bool
```
