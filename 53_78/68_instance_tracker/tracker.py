from weakref import WeakSet


def instance_tracker(*outer_args):
    name = outer_args[0] if len(outer_args) else 'instances'

    class Super:

        def __new__(cls, *args, **kwargs):
            obj = super().__new__(cls)
            getattr(obj, name).add(obj)
            return obj

    setattr(Super, name, WeakSet())

    return Super
