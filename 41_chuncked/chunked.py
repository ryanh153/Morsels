from itertools import zip_longest


SENTINAL = object()

# No libraries
#def chunked(iterable, n, *, fill=sentinal):
#     next_list = []
#     for val in iterable:
#         next_list.append(val)
#         if len(next_list) >= n:
#             yield next_list
#             next_list = []
#     if next_list:
#         if fill is not sentinal:
#             for _ in range(n-len(next_list)):
#                 next_list.append(fill)
#         yield next_list


# Some libraries and slight compact
def chunked(iterable, n, *, fill=SENTINAL):
    for next_tuple in zip_longest(*([iter(iterable)] * n), fillvalue=SENTINAL):
        if SENTINAL not in next_tuple:
            yield next_tuple
        elif fill is SENTINAL:
            yield tuple(v for v in next_tuple if v is not SENTINAL)
        else:
            yield tuple(v if v is not SENTINAL else fill for v in next_tuple)
