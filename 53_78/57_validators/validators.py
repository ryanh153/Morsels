from abc import abstractmethod, ABCMeta


class Validator(metaclass=ABCMeta):

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, owner):
        try:
            return getattr(obj, self.private_name)
        except AttributeError:
            if self.value:
                return self.value
            else:
                raise AttributeError("Value is not set")

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @staticmethod
    @abstractmethod
    def validate(value):
        raise NotImplementedError


class PositiveNumber(Validator):

    def __init__(self, value=None):
        self.value = value

    @staticmethod
    def validate(value):
        if value <= 0:
            raise ValueError(f"Value must be positive ('passed {value}")

