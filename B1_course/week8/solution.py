from itertools import chain


def multiziperator(*iterables):
    yield from chain.from_iterable(zip(*iterables))
