from inspect import signature


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
    result = ''  # blank in case no arguments passed
    if len(args):  # join the repr of all args
        result += ', '.join([repr(arg) for arg in args])
    if len(kwargs) and len(args):  # If we have args and kwargs join them with a comma
        result += ', ' + ', '.join([f'{key}={value!r}' for key, value in kwargs.items()])
    elif len(kwargs):  # Otherwise just add the kwarg representation (no single quotes around keys)
        result += ', '.join([f'{key}={value!r}' for key, value in kwargs.items()])
    return result


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


# noinspection PyPep8Naming
class auto_repr:
    """
    Class decorator that adds a __repr__ method based on the args/kwargs passed.
    :param to_decorate:
        If we are being used with no arguments the class itself will be passed to us directly. In this case infer what
        args and kwargs should be based on call signatures and return the decorated object.
        If this is None we were called with args/kwargs so we'll save them and use them when we are called
    :param args:
        An iterable of strings that are attributes of the class and passed to it's __init__ as positional arguments
    :param kwargs
        An iterable of strings that are attributes of the class and passed in to it's __init__ as keyword arguments
    """

    def __new__(cls, to_decorate=None, args=None, kwargs=None):
        # We are being called with not arguments. Want to add repr and return decorated class now
        if to_decorate is not None:
            # Get data to put in repr (all as keyword args)
            kwargs = [key for key in signature(to_decorate.__init__).parameters if key is not 'self']
            setattr(to_decorate, '__repr__', make_repr(kwargs=kwargs))
            return to_decorate
        else:  # Called with arguments. Proceed as normal for class decorate with arguments
            return super().__new__(cls)

    def __init__(self, *, args=None, kwargs=None):
        self.args, self.kwargs = args, kwargs

    def __call__(self, to_decorate=None):
        """
        :param to_decorate:
            Class to decorate
        :return:
            Class with the __repr__ method set
        """
        if self.args is None and self.kwargs is None:  # Called with no arguments -> infer them
            pass

        setattr(to_decorate, '__repr__', make_repr(args=self.args, kwargs=self.kwargs))
        return to_decorate
