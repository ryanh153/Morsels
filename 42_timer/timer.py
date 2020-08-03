from datetime import datetime
from statistics import mean, median


class Timer:
    def __init__(self, function=None):
        self.function = function  # Function to decorate if being use as a decorator
        self.start, self.elapsed = None, None
        self.runs = list()
        self.min, self.max, self.mean, self.median = None, None, None, None

    def __enter__(self):
        self.start = datetime.now()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = (datetime.now() - self.start).total_seconds()
        self.runs.append(self.elapsed)
        self._update_stats()

    def _update_stats(self):
        self.min = min(self.runs)
        self.max = max(self.runs)
        self.mean = mean(self.runs)
        self.median = median(self.runs)

    def __call__(self, *args, **kwargs):
        with self as timer:
            return self.function(*args, **kwargs)
