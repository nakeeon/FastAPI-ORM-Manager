from .decorators import catch_sqlalchemy_error


class ManagerMeta(type):
    """
    Metaclass that applies the catch_sqlalchemy_error decorator to all methods
    """

    def __new__(cls, name, bases, attrs):
        # Accessing the '__orig_bases__' attribute to check for TypeVar
        orig_bases = attrs.get('__orig_bases__')
        if orig_bases:
            for base in orig_bases:
                # Check if the base is a parameterized version of Generic
                if hasattr(base, "__origin__"):
                    # Retrieve the type arguments
                    type_args = base.__args__
                    if type_args:
                        # Attach the 'model' attribute to the class
                        attrs['model'] = type_args[0]

        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, classmethod):
                attrs[attr_name] = classmethod(catch_sqlalchemy_error(attr_value.__func__))

        return super(ManagerMeta, cls).__new__(cls, name, bases, attrs)


