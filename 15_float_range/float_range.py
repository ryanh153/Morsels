import math


class float_range:
    """Yields floats from [start, stop) with step size step.
        If passed three arguments these are start, stop, step.
        If two, they are start and stop. Step is set to 1.0.
        If one, it is stop. Start and step are set to 0.0 and 1.0 respectively."""

    def __init__(self, *args):
        if len(args) == 3:
            self.start, self.stop, self.step = args
        elif len(args) == 2:
            self.start, self.stop, self.step = (args[0], args[1], 1.0)
        elif len(args) == 1:
            self.start, self.stop, self.step = (0.0, args[0], 1.0)
        else:
            raise TypeError("float_range must be called with 1, 2, or 3 arguments.")

    def __call__(self):
        next_val = self.start
        if self.start < self.stop and self.step > 0:
            while next_val < self.stop:
                yield next_val
                next_val += self.step

        elif self.start > self.stop and self.step < 0:
            while next_val > self.stop:
                yield next_val
                next_val += self.step

    def __len__(self):
        if self.start < self.stop and self.step > 0:
            return math.ceil((self.stop-self.start)/self.step)
        elif self.start > self.stop and self.step < 0:
            return math.ceil((self.start-self.stop)/abs(self.step))
        else:
            return 0

    def __iter__(self):
        return self()

    def __next__(self):
        next(self())

    def __reversed__(self):
        next_val = self.start + (len(self)-1)*self.step
        if self.start < self.stop and self.step > 0:
            while next_val >= self.start:
                yield next_val
                next_val -= self.step

        elif self.start > self.stop and self.step < 0:
            while next_val < self.start:
                yield next_val
                next_val -= self.step

    def __eq__(self, other):
        if isinstance(other, float_range) or isinstance(other, range):
            if len(self) == 0 and len(other) == 0:
                return True
            elif not self.start == other.start:
                return False
            elif not len(self) == len(other):
                return False
            elif len(self) == 1 and len(other) == 1:
                return True
            elif not self.step == other.step:
                return False
            else:
                return True
        else:
            return other == self
