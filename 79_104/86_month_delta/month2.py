from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Union


def raise_arithmatic_error(class_instance: object, other_instance: object, operation: str) -> None:
    raise TypeError(f'{type(class_instance).__name__} does not support {operation} with {type(other_instance)}')


def handle_month_overflow(month: Month) -> Month:
    while month.month > 12:
        month.year, month.month = month.year + 1, month.month - 12
    while month.month < 1:
        month.year, month.month = month.year - 1, month.month + 12
    return month


@dataclass()
class Month:
    year: int
    month: int

    def __sub__(self: Month, other: Union[Month, MonthDelta]) -> Union[Month, MonthDelta]:
        if isinstance(other, Month):
            return MonthDelta((self.year - other.year)*12 + self.month - other.month)
        elif isinstance(other, MonthDelta):
            return handle_month_overflow(Month(self.year, self.month - other.months))
        raise raise_arithmatic_error(self, other, 'subtraction')

    def __add__(self: Month, other: Union[Month, MonthDelta]) -> Month:
        if isinstance(other, MonthDelta):
            return handle_month_overflow(Month(self.year, self.month + other.months))
        raise raise_arithmatic_error(self, other, 'addition')

    def __format__(self: Month, format_spec: str) -> str:
        result = format_spec.replace('%Y', str(self.year).zfill(4))
        result = result.replace('%m', str(self.month).zfill(2))
        result = result.replace('%b', date(self.year, self.month, 1).strftime('%b'))

        return result


@dataclass()
class MonthDelta:
    months: int

    def __add__(self: MonthDelta, other: Union[Month, MonthDelta]) -> Union[Month, MonthDelta]:
        if isinstance(other, Month):
            return other + self
        elif isinstance(other, MonthDelta):
            return MonthDelta(self.months + other.months)
        raise_arithmatic_error(self, other, 'addition')

    def __sub__(self: MonthDelta, other: MonthDelta) -> MonthDelta:
        if isinstance(other, MonthDelta):
            return MonthDelta(self.months - other.months)
        raise_arithmatic_error(self, other, 'subtraction')

    def __mul__(self: MonthDelta, other: int) -> MonthDelta:
        if isinstance(other, int):
            return MonthDelta(self.months*other)
        raise_arithmatic_error(self, other, 'multiplication')

    def __rmul__(self: MonthDelta, other: int) -> MonthDelta:
        return self.__mul__(other)

    def __truediv__(self: MonthDelta, other: MonthDelta) -> float:
        if isinstance(other, MonthDelta):
            return self.months/other.months
        raise_arithmatic_error(self, other, 'true division')

    def __floordiv__(self: MonthDelta, other: Union[int, MonthDelta]) -> Union[float, MonthDelta]:
        if isinstance(other, MonthDelta):
            return self.months // other.months
        if isinstance(other, int):
            return MonthDelta(self.months // other)
        raise_arithmatic_error(self, other, 'floor division')

    def __mod__(self: MonthDelta, other: Union[MonthDelta, int]) -> Union[float, MonthDelta]:
        if isinstance(other, MonthDelta):
            return self.months % other.months
        if isinstance(other, int):
            return MonthDelta(self.months % other)
        raise_arithmatic_error(self, other, 'modulo division')

    def __neg__(self: MonthDelta) -> MonthDelta:
        return MonthDelta(-self.months)
