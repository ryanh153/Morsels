import re
from functools import singledispatch


@singledispatch
def natural_key(item):
    raise TypeError(f'Calling natural_key with unknown type {type(item)}')


@natural_key.register(str)
def _string_key(string):
    return tuple(int(s) if s.isdigit() else s for s in re.split(f'(\d+)', string.lower()))


def natural_sort(strings, reverse=False, key=natural_key):
    return sorted(strings, reverse=reverse, key=key)
