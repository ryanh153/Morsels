from time import perf_counter
from statistics import mean, median


class Timer:
    def __init__(self, function=None):
        self.function = function  # Function to decorate if being use as a decorator
        self.start, self.elapsed, self.runs = None, None, list()

    @property
    def min(self):
        return min(self.runs)

    @property
    def max(self):
        return max(self.runs)

    @property
    def mean(self):
        return mean(self.runs)

    @property
    def median(self):
        return median(self.runs)

    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = perf_counter() - self.start
        self.runs.append(self.elapsed)

    def __call__(self, *args, **kwargs):
        with self:
            return self.function(*args, **kwargs)
