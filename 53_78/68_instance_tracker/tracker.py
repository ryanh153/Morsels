from weakref import WeakSet


def instance_tracker(*outer_args):
    """Return a class that can be inherited from and tracks all instances of that class

    :param
    outer_args:
        If an argument is passed it will be the name of the attribute [str] the instances are stored on.
        All other arguments will be ignored."""
    name = outer_args[0] if len(outer_args) else 'instances'

    class Super:
        """
        Class to be inherited from. Has an attribute where objects that are instances of child classes are stored as weak
        references.
        """
        def __new__(cls, *args, **kwargs):
            obj = super().__new__(cls)
            getattr(obj, name).add(obj)
            return obj

    setattr(Super, name, WeakSet())

    return Super
