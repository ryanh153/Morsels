from typing import Union, Any, Callable


def threshold_equal(attr_str: str, threshold: float = 2.0) -> Callable[[type], object]:
    """Class decorator with arguments. When comparing equality of instances of the decorated
    class the given attribute and tolerance will be used."""

    def decorated_class(cls: type) -> object:
        """Add the appropriate equality method to the class being decorated"""
        # Note: NotImplementedType is not in python 3.9 (will be in python 3.10). Using Any as is standard practice
        def equality_func(curr: object, other: object) -> Union[bool, Any]:
            """Equal if the given attribute difference is less than or equal to the tolerance"""
            if isinstance(other, cls):
                return abs(getattr(curr, attr_str) - getattr(other, attr_str)) <= threshold
            return NotImplemented

        setattr(cls, '__eq__', equality_func)
        return cls
    return decorated_class
