from collections import deque


def window(iterable, n, *, fillvalue=None):
    if n == 0:  # return nothing if n==0
        return

    iterator = iter(iterable)  # set up iterable and deque
    current = deque(maxlen=n)

    for _ in range(n):  # get first return
        current.append(next(iterator, fillvalue))
    yield tuple(current)

    for val in iterator:  # yield further returns
        current.append(val)
        if len(current) == n:
            yield tuple(current)
