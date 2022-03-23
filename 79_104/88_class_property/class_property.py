from functools import partial


class class_property:

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, obj_type=None):
        assert obj_type is not None
        return self.func(obj_type)


class class_only_property:

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, obj_type=None):
        if obj is not None:
            raise AttributeError(f'{self.__name__} cannot be called on an instance. Just the class')
        return self.func(obj_type)


class class_only_method:

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, obj_type=None):
        if obj is not None:
            raise AttributeError(f'{self.__name__} cannot be called on an instance. Just the class')
        new_func = partial(self.func, obj_type)
        new_func.__doc__ = self.func.__doc__
        return new_func
