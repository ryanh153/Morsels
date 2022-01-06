from inspect import signature
from itertools import chain


def format_arguments(*args, **kwargs) -> str:
    """
    Make a string representation of any number of positional and keyword arguments
    :param args:
        A tuple of positional arguments of any type
    :param kwargs:
        A dictionary of keyword arguments of any type
    :return:
        A string representation of the inputs
    """
    return ', '.join(chain([f'{arg!r}' for arg in args],
                           [f'{key}={value!r}' for key, value in kwargs.items()]))


def make_repr(*, args=None, kwargs=None):
    """
    Returns a function which when called with an instance of class will return a string representation of the class
    :param args:
        An iterable of strings that are attributes of the class and passed to it's __init__ as positional arguments
    :param kwargs
        An iterable of strings that are attributes of the class and passed in to it's __init__ as keyword arguments
    :return:
        A function which can be passed an instance of the class and return its string representation
    """
    def make_string_repr(instance):
        """
        Function to return. Takes an instance of the class and returns its string representation
        :param instance:
            Class instance. args and kwargs will be iterated over and the values of those attribute names will be found.
            Any that are not found must have a default value. These will not be included in the repr.
            If attributes are not found and don't have a default a TypeError will be raise (through the bind call)
        :return:
            String representation of the instance
        """
        arg_list = [] if args is None else [getattr(instance, arg) for arg in args if hasattr(instance, arg)]

        kwarg_dict = {} if kwargs is None else {key: getattr(instance, key) for key in kwargs if hasattr(instance, key)}

        # Check that we could bind the args/kwargs that found matches to the __init__ method
        # Basically this is checking that any arguments we didn't find on the instance have default values
        signature(instance.__class__).bind(*arg_list, **kwarg_dict)

        return instance.__class__.__name__ + '(' + format_arguments(*arg_list, **kwarg_dict) + ')'

    return make_string_repr


def auto_repr(cls=None, /, *, args=None, kwargs=None):
    """
    Class decorator that can optionally take arg/kwargs that are expected to be class attributes.
    If they are not given they will be inferred from the class' __init__ signature
    :param cls:
        Class to be decorated (if not arguments passed). Position only
    :param args:
        Position arguments that appear as class attributes
    :param kwargs:
        Keyword arguments that appear as class attributes
    :return:
        The class with the __repr__ function added (if cls passed) or a decorator that accepts a class and then
        decorates it using args/kwargs
    """
    if cls is not None:  # infer parameters and return decorated class
        kwargs = [key for key in signature(cls.__init__).parameters if key is not 'self']  # skip self
        setattr(cls, '__repr__', make_repr(kwargs=kwargs))
        return cls

    # Otherwise we were passed the parameters. Return a decorator function that uses them
    def decorator(to_decorate):
        setattr(to_decorate, '__repr__', make_repr(args=args, kwargs=kwargs))
        return to_decorate

    return decorator
