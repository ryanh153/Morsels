import inspect
import functools
import pdb


def debug_calls(func=None, *, set_break=None):
    # If we're called with an argument we don't get the function (it's not passed)
    # So return a version of ourselves with set break set accordingly
    # That will be called and we'll be good
    if func is None:
        return functools.partial(debug_calls, set_break=set_break)

    # Set non-locals
    first = True
    condition = ''

    @functools.wraps(func)
    def inner(*args, **kwargs):
        nonlocal first, condition, set_break
        break_set = False
        frame_info = inspect.getouterframes(inspect.currentframe(), 2)[1]
        # Put our arguments into the local namespace
        call_dict = {name: value for name, value in
                     zip(inspect.getfullargspec(func).args, args)}
        call_dict.update(kwargs)
        locals().update(call_dict)

        # Set condition if doing so
        if first and set_break:
            condition = input(f'Debug {func.__name__} when?: ')
            first = False

        # Check for breaks
        if set_break and eval(condition):
            print(f'Condition met: {condition}')
            break_set = True

        elif set_break and not eval(condition):
            print(f'Condition not met: {condition}')

        first = False
        print(f'{func.__name__}('
              f'{", ".join([repr(arg) for arg in args])}'
              f'{", " if len(args) and len(kwargs) else ""}'
              f'{", ".join(f"{str(key)}={repr(val)}" for key, val in kwargs.items())}'
              f') called by '
              f'{frame_info.function} '
              f'in file {frame_info.filename} '
              f'on line {frame_info.lineno}')

        if break_set:
            return pdb.runcall(func, *args, **kwargs)
        else:
            return func(*args, **kwargs)

    return inner
