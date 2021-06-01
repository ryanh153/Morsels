from typing import Union, Any


class threshold_equal:
    """Class decorator with arguments. When comparing equality of instances of the decorated
    class the given attribute and tolerance will be used."""

    def __init__(self, attr_str: str, threshold: float = 2.0) -> None:
        """attr_str: The name of the attribute to be used when comparing equality
    threshold: The tolerance (absolute) on the attributes value"""
        self.attr_str = attr_str
        self.threshold = threshold

    def __call__(self, cls: type) -> object:
        """Add the appropriate equality method to the class being decorated"""
        # Note: NotImplementedType is not in python 3.9 (will be in python 3.10). Using Any as is standard practice
        def equality_func(curr: object, other: object) -> Union[bool, Any]:
            """Equal if the given attribute difference is less than or equal to the tolerance"""
            if isinstance(other, cls):
                return abs(getattr(curr, self.attr_str) - getattr(other, self.attr_str)) <= self.threshold
            return NotImplemented

        setattr(cls, '__eq__', equality_func)
        return cls
