import re
import sys
from functools import partial


smoosh_pattern = r'smo(o+)sh'


def is_iterable(item):
    return hasattr(item, '__iter__') and not isinstance(item, str)


def smoosh(iterable, depth=0, max_depth=1):
    result = list()
    for item in iterable:
        if is_iterable(item) and depth < max_depth:
            result += smoosh(item, depth=depth+1, max_depth=max_depth)
        else:
            result.append(item)

    return result


__path__ = sys.path
__all__ = ['smoo' + 'o'*i + 'sh' for i in range(9)]


def __getattr__(name):
    if m := re.fullmatch(smoosh_pattern, name):
        return partial(smoosh, max_depth=len(m.groups()[0]))
    return globals()[name]


def __dir__():
    return set(__all__)
