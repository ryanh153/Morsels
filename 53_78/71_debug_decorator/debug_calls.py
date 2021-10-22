import inspect
import functools
import pdb


def make_call_string(func, *args, **kwargs):
    frame_info = inspect.getouterframes(inspect.currentframe(), 2)[2]
    return f'{func.__name__}('\
           f'{", ".join([repr(arg) for arg in args])}'\
           f'{", " if len(args) and len(kwargs) else ""}'\
           f'{", ".join(f"{str(key)}={repr(val)}" for key, val in kwargs.items())}'\
           f') called by '\
           f'{frame_info.function} '\
           f'in file {frame_info.filename} '\
           f'on line {frame_info.lineno}'


def debug_calls(func=None, *, set_break=False):

    def decorator(function):

        @functools.wraps(function)
        def inner(*args, **kwargs):
            print(make_call_string(function, *args, **kwargs))

            if set_break:
                if not inner.break_condition:
                    inner.break_condition = input(f'Debug {function.__name__} when?: ')

                # Get bound function namespace for eval
                signature = inspect.signature(function).bind(*args, **kwargs)
                signature.apply_defaults()

                if eval(inner.break_condition, signature.arguments):
                    print(f'Condition met: {inner.break_condition}')
                    return pdb.runcall(function, *args, **kwargs)
                else:
                    print(f'Condition not met: {inner.break_condition}')

            return function(*args, **kwargs)

        inner.break_condition = None
        return inner

    if func is None:  # Called w/ arguments. Return decorator to be called
        return decorator
    else:  # Called as decorator with no arguments
        return decorator(func)
