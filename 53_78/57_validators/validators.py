import uuid
from abc import ABCMeta, abstractmethod

MISSING = object()


class Validator(metaclass=ABCMeta):

    def __init__(self, initial=MISSING):
        self.initial = initial
        self.name = '_' + str(uuid.uuid4().hex)

    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, obj, owner):
        if self.initial is MISSING:
            return getattr(obj, self.name)
        else:
            return getattr(obj, self.name, self.initial)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.name, value)

    @staticmethod
    @abstractmethod
    def validate(value):
        raise NotImplementedError


class PositiveNumber(Validator):

    @staticmethod
    def validate(value):
        if value <= 0:
            raise ValueError(f"Value must be positive ('passed {value}")
