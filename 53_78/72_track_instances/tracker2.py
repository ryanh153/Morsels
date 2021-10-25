from weakref import WeakSet
from functools import partial


def track_instances(cls_or_str):

    def class_decorator(cls, name):

        def init(self, *args, **kwargs):
            getattr(self, name).add(self)
            super(Temp, self).__init__(*args, **kwargs)

        Temp = type('Temp', (cls,), {'__init__': init, name: WeakSet()})
        return Temp

    if isinstance(cls_or_str, str):
        return partial(class_decorator, name=cls_or_str)
    return class_decorator(cls_or_str, name='instances')


class InstanceTracker(type):
    def __new__(cls, name, bases, attrs):
        tracked = super(InstanceTracker, cls).__new__(cls, name, bases, attrs)
        tracked.instances = WeakSet()

        def init(self, *args, **kwargs):
            getattr(self, 'instances').add(self)
            attrs['__init__'](self, *args, **kwargs)

        tracked.__init__ = init
        return tracked

    def __iter__(self):
        return iter(self.instances)
