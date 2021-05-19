from __future__ import annotations

from typing import Union

numeric = Union[int, float]


class ThresholdEqual:
    """Stores a value and a threshold (default zero) for comparing equality"""

    def __init__(self, value: numeric, threshold: numeric = 2) -> None:
        """Takes value (numeric) and an optional threshold to be used in comparisons"""
        self.value = value
        self.threshold = threshold

    def __eq__(self, other: object) -> bool:
        """If other is numeric and the difference between it and our value is within the threshold return True"""
        if isinstance(other, ThresholdEqual):
            return abs(self.value - other.value) <= self.threshold
        return NotImplemented

    # Implement all relevant mathematics operations
    def __add__(self, other: ThresholdEqual) -> numeric:
        if isinstance(other, ThresholdEqual):
            return self.value + other.value
        return NotImplemented

    def __sub__(self, other: ThresholdEqual) -> numeric:
        if isinstance(other, ThresholdEqual):
            return self.value - other.value
        return NotImplemented

    def __mul__(self, other: ThresholdEqual) -> numeric:
        if isinstance(other, ThresholdEqual):
            return self.value * other.value
        return NotImplemented

    def __truediv__(self, other: ThresholdEqual) -> numeric:
        if isinstance(other, ThresholdEqual):
            return self.value / other.value
        return NotImplemented

    def __mod__(self, other: ThresholdEqual) -> numeric:
        if isinstance(other, ThresholdEqual):
            return self.value % other.value
        return NotImplemented

    def __pow__(self, other: ThresholdEqual) -> numeric:
        if isinstance(other, ThresholdEqual):
            return self.value ** other.value
        return NotImplemented
