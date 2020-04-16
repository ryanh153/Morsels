from itertools import zip_longest


def interleave(*iters):
    ###
    # sentinel = object()
    # for t in zip_longest(*iters, fillvalue=sentinel):
    #     for el in t:
    #         if el != sentinel:
    #             yield el
    ###
    # sentinel = object()
    # return (
    #     el
    #     for t in zip_longest(*iters, fillvalue=sentinel)
    #     for el in t
    #     if el != sentinel
    #         )
    ###
    iter_list = [iter(i) for i in iters]  # get a list of iterators over each iterable passed
    while iter_list:  # as long as we have an iterator left
        for iterable in list(iter_list):  # iterates from copy so order isn't messed up if we remove
            try:
                yield next(iterable)
            except StopIteration:
                iter_list.remove(iterable)
                