def strict_zip(*sequences):
    """Zip an arbitrary number of iterables that are the same length together."""
    iterators = [iter(s) for s in sequences]
    while next_tuple := get_next(iterators):
        yield next_tuple


def get_next(iterators):
    """Make a tuple that is the next element of each iterator. If only some have a next value raise a value error"""
    result = []
    for i in iterators:
        try:
            result.append(next(i))
        except StopIteration:
            pass
    if len(result) == len(iterators) or not len(result):
        return tuple(result)
    raise ValueError('Value out of range')