sentinal = object()


def chunked(iterable, n, *, fill=sentinal):
    next_list = []
    for val in iterable:
        next_list.append(val)
        if len(next_list) >= n:
            yield next_list
            next_list = []
    if next_list:
        if fill is not sentinal:
            for _ in range(n-len(next_list)):
                next_list.append(fill)
        yield next_list
