def multiziperator(*iterables):
    iters = [iter(val) for val in iterables]
    while True:
        try:
            curr = [next(i) for i in iters]
            yield from curr
        except StopIteration:
            return


res = multiziperator('abcd', 'efg')
print(list(res))
