from weakref import WeakSet
from functools import partial


def track_instances(cls_or_str):

    def class_decorator(cls, name):
        def __init__(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            getattr(self, name).add(self)

        setattr(cls, name, WeakSet())
        original_init = cls.__init__
        cls.__init__ = __init__
        return cls

    if isinstance(cls_or_str, str):
        return partial(class_decorator, name=cls_or_str)
    return class_decorator(cls_or_str, name='instances')


class InstanceTracker(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)  # Construct from our parent (type)
        cls._instances = WeakSet()

    def __call__(cls, *args, **kwargs):
        # This is called when an instance of the class using us for a meta is made
        instance = super().__call__(*args, **kwargs)  # Again rely on type to do the normal stuff
        cls._instances.add(instance)
        return instance

    def __iter__(cls):
        yield from cls._instances
