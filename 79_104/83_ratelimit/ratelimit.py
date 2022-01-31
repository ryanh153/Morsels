import time
from functools import wraps
from collections import deque
from contextlib import contextmanager


class ratelimit:

    def __init__(self, per_second, sleep=False):
        self.per_second = per_second
        self.sleep = sleep

    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            # nonlocal sleep
            now = time.perf_counter()
            # if len(calls):
            #     print(f'We have a queue of size {len(calls)} and the total time span is {(now - calls[0])}')
            if len(calls) == per_second and (now - calls[0]) < 1.0:
                if sleep:
                    time.sleep(1.0 - (now - calls[0]))  # Wait for one second since first call in sequence
                else:
                    raise Exception(f'{func} called more than {per_second} times in a second')
            calls.append(now)
            return func(*args, **kwargs)

def ratelimit(per_second, sleep=False):
    calls = deque(maxlen=per_second)

    def decorator(func):

        @wraps(func)
        def inner(*args, **kwargs):
            # nonlocal sleep
            now = time.perf_counter()
            # if len(calls):
            #     print(f'We have a queue of size {len(calls)} and the total time span is {(now - calls[0])}')
            if len(calls) == per_second and (now - calls[0]) < 1.0:
                if sleep:
                    time.sleep(1.0 - (now-calls[0]))  # Wait for one second since first call in sequence
                else:
                    raise Exception(f'{func} called more than {per_second} times in a second')
            calls.append(now)
            return func(*args, **kwargs)

        return inner

    try:
        yield decorator
    finally:
        calls = deque(maxlen=per_second)
