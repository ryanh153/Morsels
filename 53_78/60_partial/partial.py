import functools

SKIP = object()


class partial(functools.partial):
    def __call__(self, *fargs, **fkwargs):
        final_args = replace_skips(self.args, fargs)
        return self.func(*final_args, **self.keywords, **fkwargs)

    def partial(self, *args, **kwargs):
        return partial(self.func, *self.args, *args, **{**self.keywords, **kwargs})


def replace_skips(initial_args, new_args):
    if len(new_args) < initial_args.count(SKIP):
        raise TypeError("Not enough positional arguments")
    new_args = list(new_args[::-1])  # make reversed for more efficient popping
    final_args = [val if val is not SKIP else new_args.pop() for val in initial_args]
    return final_args + new_args[::-1]  # add on un-consumed arguments
