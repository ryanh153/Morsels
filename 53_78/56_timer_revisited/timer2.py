from time import perf_counter


_memoized = {}


def memoize(cls):
    def memoized(name=None):
        print(f'have {_memoized}\nmaking {name}')
        if name and name not in _memoized:
            _memoized[name] = cls()
            return _memoized[name]
        elif name:
            return _memoized[name]
        else:
            return cls()
    return memoized


@memoize
class Timer:

    def __init__(self):
        self.start, self.stop, self.elapsed = None, None, None
        self.splits, self.runs = [], []
        self.stored_runs = {}

    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop = perf_counter()
        self.elapsed = self.stop - self.start
        self.runs.append(self.elapsed)
        self.start, self.stop = None, None

    def split(self, name=None):
        if self.start is None:
            raise RuntimeError('Timer is not running!')
        if name:
            if name not in self.stored_runs:
                new_timer = Timer()
                self.stored_runs[name] = new_timer
            return self.stored_runs[name]
        else:
            new_timer = Timer()
            self.splits.append(new_timer)
            return new_timer

    def __getitem__(self, key):
        if isinstance(key, str):
            return self.stored_runs[key]
        elif isinstance(key, int):
            return self.splits[key]
        return NotImplemented
