from functools import singledispatch
from pathlib import Path


def natural_key(item):
    result = []
    for p in item.split():
        try:
            result.append(int(p))
        except ValueError:
            result.append(p.lower())
    return tuple(result)


@singledispatch
def natural_sort(strings, reverse=False, key=natural_key):
    return sorted(strings, reverse=reverse, key=key)


# @natural_sort.register(Path)
# def _(path, reverse=False, key=natural_key):
#     print(path.parts)
#     return natural_sort(path.parts, reverse, key)


print(natural_sort(['take 8', 'take 11', 'take 9', 'take 10', 'take 1']))
print(natural_sort(['02', '1', '16', '17', '20', '26', '3', '30']))
print(natural_sort(Path('.').absolute()))
