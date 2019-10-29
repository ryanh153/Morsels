# base
# def compact(raw_seq):
#     to_return = []
#
#     for pair in zip(reversed(raw_seq), reversed(raw_seq[:-1])):
#         if pair[0] != pair[1]:
#             to_return.append(pair[0])
#
#     if len(raw_seq) > 0:
#         to_return.append(raw_seq[0])
#
#     return list(reversed(to_return))

# Bonus 1
# def compact(raw_seq):
#     to_return = []
#
#     for val in raw_seq:
#         if len(to_return) == 0:
#             to_return.append(val)
#         else:
#             if val != prev_val:
#                 to_return.append(val)
#         prev_val = val
#
#     return to_return

# Bonus 2/final


def compact(raw_seq):
    """Takes in any iterable and yields (generator) a sequence where repeated values are ignored.
    Ex: [1,1,2,2,3] -> 1,2,3"""
    prev_val = None
    for val in raw_seq:
        if prev_val is None:
            yield(val)
        else:
            if val != prev_val:
                yield(val)
        prev_val = val

