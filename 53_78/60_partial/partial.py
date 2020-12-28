SKIP = object()


class partial:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = list(args)
        self.kwargs = kwargs

    def __call__(self, *fargs, **fkwargs):
        final_args = replace_skips(self.args, fargs)
        return self.func(*final_args, **self.kwargs, **fkwargs)

    def __repr__(self):
        args_str = ', '.join(repr(val) for val in self.args)
        kwargs_str = ', '.join(f'{repr(key)}={repr(val)}' for key, val in self.kwargs.items())
        return f'<{self.func.__name__}, {args_str}, {kwargs_str}>'

    def partial(self, *args, **kwargs):
        new_args = self.args + list(args)
        new_kwargs = self.kwargs.copy()
        new_kwargs.update(kwargs)
        return partial(self.func, *new_args, **new_kwargs)


def replace_skips(initial_args, new_args):
    fargs_iter = iter(new_args)
    final_args = []
    for temp_arg in initial_args:
        if temp_arg is SKIP:
            try:
                temp_arg = next(fargs_iter)  # fill in ones we skipped
            except StopIteration:
                raise TypeError("Not enough positional arguments")
        final_args.append(temp_arg)

    final_args += [val for val in fargs_iter]  # add on un-consumed arguments
    return final_args
