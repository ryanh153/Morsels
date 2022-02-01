import time
from functools import wraps
from collections import deque


class ratelimit:

    def __init__(self, per_second, sleep=False):
        self.per_second = per_second
        self.sleep = sleep
        self.calls = deque(maxlen=self.per_second)

    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            self.called(func)
            return func(*args, **kwargs)
        return inner

    def called(self, func):
        now = time.perf_counter()
        if len(self.calls) == self.per_second and (now - self.calls[0]) < 1.0:
            if self.sleep:
                time.sleep(1.0 - (now - self.calls[0]))  # Wait for one second since first call in sequence
                now = time.perf_counter()  # Update to real time the call happens
            else:
                raise Exception(f'{func} called more than {self.per_second} times in a second')
        self.calls.append(now)

    def __enter__(self):
        self.called(None)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
