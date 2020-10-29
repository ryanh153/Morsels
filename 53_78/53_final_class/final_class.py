class UnsubclassableType(type):
    def __new__(cls, name, bases, namespace):
        if any(type(b) == UnsubclassableType for b in bases):
            raise TypeError(f'Class {cls.__name__} is not a valid base class')
        return super().__new__(cls, name, bases, namespace)


def final_class(cls):
    @classmethod
    def no_subclass(subclass):
        raise TypeError(f'Class {subclass.__name__} is trying to inherit from Class {cls.__name__} which is not allowed')
    cls.__init_subclass__ = no_subclass
    return cls


@final_class
class Unsubclassable():
    pass
