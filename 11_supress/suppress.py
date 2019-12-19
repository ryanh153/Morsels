import functools


class suppress(object):

    def __init__(self, *args):
        self.error_types = []
        for arg in args:
            self.error_types.append(arg)
        self.exception = None
        self.traceback = None

    def __enter__(self):
        return self

    def __exit__(self, caught_error, caught_value, traceback):

        if caught_error is None or\
                any([issubclass(caught_error, error_type) for error_type in self.error_types]):
            self.exception = caught_value
            self.traceback = traceback
            return True
        else:
            raise caught_error

    def __call__(self, func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return decorated
