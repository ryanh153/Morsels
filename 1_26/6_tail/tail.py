import collections

# def tail(seq, n):
#     """Takes sequence (seq) and integer (n). Returns last n items in seq."""
#
#     result = []
#     if n > 0:
#         result = list(collections.deque(seq, maxlen=n))
#
#     return result

def tail(seq, n):
    """Takes sequence (seq) and integer (n). Returns last n items in seq."""

    if n <= 0:
        return []
    else:
        return list(collections.deque(seq, maxlen=n))