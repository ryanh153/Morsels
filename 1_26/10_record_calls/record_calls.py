import functools
from dataclasses import dataclass
from typing import Any, Optional

NO_RETURN = object()

@dataclass
class Call:
    args: tuple
    kwargs: dict
    return_value: Any = NO_RETURN  # type is any, default is NO_RETURN
    exception: Optional[BaseException] = None  # type is optionally BaseException, but its default it none


def record_calls(func):
    """Decorator to track number of times a function is called"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1  # these three are the same whether or not exception is thrown
        call = Call(args, kwargs)
        wrapper.calls.append(call)
        try:  # return_value and exception depend on success of call
            call.return_value = func(*args, **kwargs)
        except Exception as ex:
            call.exception = ex
            raise ex  # raise exception
        return call.return_value

    # Set up defaults
    wrapper.call_count = 0
    wrapper.calls = []  # will be a list of named tuples

    return wrapper
