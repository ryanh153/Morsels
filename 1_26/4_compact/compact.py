# base
# def compact(raw_seq):
#     to_return = []
#
#     for i, item in enumerate(raw_seq):
#         if i == 0 or item != raw_seq[i-1]:
#             to_return.append(item)
#
#     return to_return

# Bonus 1
# def compact(raw_seq):
#     to_return = []
#     prev_val = object()
#
#     for val in raw_seq:
#         if val != prev_val:
#             to_return.append(val)
#         prev_val = val
#
#     return to_return

# Bonus 2/final


def compact(raw_seq):
    """Takes in any iterable and yields (generator) a sequence where repeated values are ignored.
    Ex: [1,1,2,2,3] -> 1,2,3"""

    prev_val = object()
    for val in raw_seq:
        if val != prev_val:
            yield(val)
        prev_val = val
