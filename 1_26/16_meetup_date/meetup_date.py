from calendar import monthcalendar
from datetime import date
from enum import IntEnum


class Weekday(IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


def meetup_date(year, month, nth=4, weekday=Weekday.THURSDAY):
    """Get the nth weekday of the month given. Default is 4th thursday."""
    cal = monthcalendar(year, month)
    # look forward and day not in first week or look back and it's in the last week
    if (nth > 0 and not cal[0][weekday]) or (nth < 0 and cal[-1][weekday]):
        return date(year, month, cal[nth][weekday])
    else:
        return date(year, month, cal[nth-1][weekday])
