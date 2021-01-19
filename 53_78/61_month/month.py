from functools import total_ordering
import datetime
from calendar import monthrange
import inspect


@total_ordering
class Month:
    __slots__ = ['year', 'month', 'month_str', 'first_day', 'last_day']

    def __init__(self, year, month):
        self.year = year
        self.month = month
        if self.month < 10:
            self.month_str = f'0{month}'
        else:
            self.month_str = str(month)

        _, last = monthrange(year, month)
        self.first_day = datetime.date(year, month, 1)
        self.last_day = datetime.date(year, month, last)

    @staticmethod
    def from_date(date):
        instance = Month(date.year, date.month)
        return instance

    def strftime(self, format):
        return self.first_day.strftime(format)

    def __str__(self):
        return f'{self.year}-{self.month_str}'

    def __repr__(self):
        return f'{type(self).__name__}({self.year}, {self.month})'

    def __eq__(self, other):
        if not isinstance(other, Month):
            return NotImplemented
        return self.year == other.year and self.month == other.month

    def __lt__(self, other):
        if not isinstance(other, Month):
            return NotImplemented
        if self.year < other.year:
            return True
        elif self.year == other.year and self.month < other.month:
            return True
        else:
            return False

    def __setattr__(self, *args):
        if inspect.stack()[1][3] == '__init__':
            object.__setattr__(self, *args)
        else:
            raise TypeError(f'{type(self).__name__} is immutable')

    def __delattr__(self, item):
        raise TypeError(f'{type(self).__name__} is immutable')

    def __hash__(self):
        return hash(repr(self))
