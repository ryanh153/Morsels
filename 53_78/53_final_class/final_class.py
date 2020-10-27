class UnsubclassableType(type):
    def __new__(mcs, name, base, dct):
        for b in base:
            if type(b) == mcs:
                raise TypeError(f'Class {b.__name__} cannot be inherited from')
        new_cls = super().__new__(mcs, name, base, dct)
        return new_cls


class Unsubclassable(metaclass=UnsubclassableType):
    pass


class final_class():
    def __init__(self, name, base=(), dct=None):
        for b in base:
            if type(b) == type(self):
                raise TypeError('Can not sub from class decorated by final_class')
        self.decorated_class = name

    def __call__(self, *args, **kwargs):
        return self.decorated_class(*args, **kwargs)
