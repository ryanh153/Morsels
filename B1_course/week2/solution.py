def interp_args(start, stop, step):
    if stop is None:
        start, stop = 0, start
    return start, stop, step


def myrange(start, stop, step):
    val = start
    while val < stop:
        yield val
        val += step


def myrange2(start, stop=None, step=1):
    start, stop, step = interp_args(start, stop, step)
    # return list(range(start, stop, step))
    return list(myrange(start, stop, step))


def myrange3(start, stop=None, step=1):
    start, stop, step = interp_args(start, stop, step)
    # yield from range(start, stop, step)
    yield from myrange(start, stop, step)
