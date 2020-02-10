from collections.abc import Sequence


def window(iterable, n, *, fillvalue=None):
    held_list, start = [], -1
    if n == 0:
        yield from []
    elif isinstance(iterable, Sequence):
        if n > len(iterable):
            iterable += [fillvalue for _ in range(n-len(iterable))]
        yield from [tuple(iterable[i:i+n]) for i in range(len(iterable)-(n-1))]
    else:
        while True:
            start += 1
            stop = start + n
            try:
                held_list += [next(iterable) for _ in range(stop - len(held_list))]
                yield tuple(held_list[start:stop])
            except StopIteration:
                break
