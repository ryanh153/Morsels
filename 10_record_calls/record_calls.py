import functools
from collections import namedtuple

NO_RETURN = object()


def record_calls(func):
    """Decorator to track number of times a function is called"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls.append(namedtuple("Call", "args, kwargs, return_value, exception"))  # new named tuple
        wrapper.call_count += 1  # these three are the same whether or not exception is thrown
        wrapper.calls[-1].args = args
        wrapper.calls[-1].kwargs = kwargs
        try:  # return_value and exception depend on success of call
            value = func(*args, **kwargs)
            wrapper.calls[-1].return_value = value  # capture value
            wrapper.calls[-1].exception = None  # no exception
        except Exception as ex:
            wrapper.calls[-1].return_value = NO_RETURN  # unique value to show what happened
            wrapper.calls[-1].exception = ex  # capture exception
            raise ex  # raise exception
        return value

    # Set up defaults
    wrapper.call_count = 0
    wrapper.calls = []  # will be a list of named tuples

    return wrapper


@record_calls
def greet(name):
    """Test func"""
    print(f"Hello {name}")
