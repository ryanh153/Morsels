from itertools import zip_longest


SENTINAL = object()


# Some libraries and slight compact
def chunked(iterable, n, *, fill=SENTINAL):
    iterables = [iter(iterable)] * n
    chunks = zip_longest(*iterables, fillvalue=fill)
    return ([val for val in chunk if val is not SENTINAL] for chunk in chunks)
