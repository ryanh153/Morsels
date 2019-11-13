# import collections
#
#
# def tail(seq, n):
#     """Takes sequence (seq) and integer (n). Returns last n items in seq."""
#
#     if n > 0:
#         result = collections.deque(maxlen=n)
#         for item in seq:
#             result.append(item)
#     else:
#         result = []
#
#     return list(result)