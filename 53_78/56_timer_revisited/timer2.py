from time import perf_counter


class Timer:
    named_timers = {}

    def __new__(cls, name=None):
        if name is None:
            return super().__new__(cls)
        elif name not in cls.named_timers:
            cls.named_timers[name] = super().__new__(cls)
        return cls.named_timers[name]

    def __init__(self, name=None):
        if not hasattr(self, 'running'):
            self.running = False
            self.start, self.stop, self.elapsed = None, None, None
            self.runs, self.splits, self.named_splits = [], [], {}

    def __enter__(self):
        self.running = True
        self.start = perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop = perf_counter()
        self.running = False
        self.elapsed = self.stop - self.start
        self.runs.append(self.elapsed)

    def split(self, name=None):
        if not self.running:
            raise RuntimeError('Timer is not running!')
        if name:
            return self.named_splits.setdefault(name, Timer())
        else:
            self.splits.append(Timer())
            return self.splits[-1]

    def __getitem__(self, key):
        if isinstance(key, str):
            return self.named_splits[key]
        return self.splits[key]
