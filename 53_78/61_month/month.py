import datetime
from calendar import monthrange
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Month:
    __slots__ = ['year', 'month', 'first_day', 'last_day']
    year: int
    month: int

    def __post_init__(self):
        _, last = monthrange(self.year, self.month)
        super().__setattr__('first_day', datetime.date(self.year, self.month, 1))
        super().__setattr__('last_day', datetime.date(self.year, self.month, last))

    @classmethod
    def from_date(cls, date):
        return cls(date.year, date.month)

    def strftime(self, fmt):
        return self.first_day.strftime(fmt)

    def __str__(self):
        return f'{self.year}-{self.month:02}'
