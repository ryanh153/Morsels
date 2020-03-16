from itertools import zip_longest


def interleave(*iters):
    SENTINEL = object()
    for t in zip_longest(*iters, fillvalue=SENTINEL):
        for el in t:
            if el != SENTINEL:
                yield el
