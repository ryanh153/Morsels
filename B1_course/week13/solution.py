from functools import total_ordering
import operator
from numbers import Real
from typing import Union, Any, Callable

# Note: NotImplementedType is not in python 3.9 (to be reintroduced in python 3.10). Using Any as is standard practice


@total_ordering
class ThresholdEqual:
    """Stores a numeric value and a threshold (default 2) for comparing equality"""

    def __init__(self, value: Real, threshold: float = 2.0) -> None:
        """Takes value (numeric) and an optional threshold to be used in comparisons
        Sets up all mathematical operations"""
        self.value = value
        self.threshold = threshold

    def __eq__(self, other: object) -> Union[bool, Any]:
        """Define equality based on value for total ordering"""
        if isinstance(other, ThresholdEqual):
            return abs(self.value - other.value) <= self.threshold
        return NotImplemented

    def __lt__(self, other: object) -> Union[bool, Any]:
        """Define less than based on value for total ordering"""
        if isinstance(other, ThresholdEqual):
            return abs(self.value - other.value) <= self.threshold
        return NotImplemented


def apply_func(func: Callable[[Real, Real], Real]) -> Callable[[ThresholdEqual, ThresholdEqual], Union[bool, Any]]:
    """Take a function that takes the value attribute two ThresholdEqual objects.
    It then returns a callable that can be passed just the ThresholdEqual objects themselves
    Used for adding methods to the ThresholdEqual class easily"""
    def inner(self: ThresholdEqual, other: ThresholdEqual) -> Union[bool, Any]:
        return func(self.value, other.value)
    return inner


for function in ['__add__', '__sub__', '__mul__', '__truediv__', '__mod__', '__pow__']:
    setattr(ThresholdEqual, function, apply_func(getattr(operator, function)))
