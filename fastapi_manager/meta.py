from .decorators import catch_sqlalchemy_error


class SQLAlchemyErrorHandlerMeta(type):
    """
    Metaclass that applies the catch_sqlalchemy_error decorator to all methods
    """

    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, classmethod):
                attrs[attr_name] = classmethod(catch_sqlalchemy_error(attr_value.__func__))

        return super(SQLAlchemyErrorHandlerMeta, cls).__new__(cls, name, bases, attrs)


