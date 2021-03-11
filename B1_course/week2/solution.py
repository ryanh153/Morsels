def myrange3(start, stop, step):
    if not step:
        start, stop = 0, start
    while start < stop:
        yield start
        start += step


def myrange2(start, stop=None, step=1):
    return list(myrange3(start, stop, step))
