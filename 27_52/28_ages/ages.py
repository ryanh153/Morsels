import calendar
from datetime import datetime
from fractions import Fraction


def is_over(age_to_comp, birth_str):
    return get_age(birth_str) >= age_to_comp


def comp_month_day(date1, date2):
    """Return true if data1 one or after date2 (regardless of year)"""
    return (date1.month, date1.day) >= (date2.month, date2.day)


def get_age(birth_str, exact=False):
    """Get age given birth date (string). If exact result is a Fraction. Else integer."""
    birth = datetime.fromisoformat(birth_str)
    now = datetime.now()
    age = now.year - birth.year if comp_month_day(now, birth) else now.year - birth.year - 1
    if exact:
        extra_days = (now-datetime(birth.year+age, birth.month, birth.day)).days
        denom = get_age_denom(birth, age)
        age = age + Fraction(extra_days, denom)
    return age


def get_age_denom(birth, age):
    """Get the number of days between the last birthday and the next birthday for someone of the given age/brithdate"""
    last_birthday = datetime(birth.year+age, birth.month, birth.day)
    next_birthday = datetime(birth.year + age + 1, birth.month, birth.day)
    # If the year of last birthday was a leap year and the birthday was before the leap day -> 366 days btwn birth days
    if calendar.isleap(last_birthday.year) and not comp_month_day(last_birthday, datetime(last_birthday.year, 2, 29)):
        return 366
    # If the year after the last birthday is a leap year and next birthday is after leap day -> 366 days btwn birth days
    elif calendar.isleap(next_birthday.year) and comp_month_day(next_birthday, datetime(next_birthday.year, 3, 1)):
        return 366
    else:
        return 365
