import math


class float_range:
    """Yields floats from [start, stop) with step size step.
        If passed three arguments these are start, stop, step.
        If two, they are start and stop. Step is set to 1.0.
        If one, it is stop. Start and step are set to 0.0 and 1.0 respectively."""

    def __init__(self, start, stop=None, step=1.):
        if stop is None:
            self.start, self.stop, self.step = 0., start, step
        else:
            self.start, self.stop, self.step = start, stop, step

    def __call__(self):
        next_val = self.start
        if len(self):
            while (self.stop - next_val)/self.step > 0:
                yield next_val
                next_val += self.step

    def __len__(self):
        if (self.stop-self.start)/self.step > 0:
            return math.ceil((self.stop-self.start)/self.step)
        else:
            return 0

    def __iter__(self):
        return self()

    def __next__(self):
        next(self())

    def __reversed__(self):
        next_val = self.start + (len(self)-1)*self.step
        if len(self):
            while (next_val-self.start)/self.step >= 0:
                yield next_val
                next_val -= self.step

    @staticmethod
    def _attrs(self):
        if len(self) == 0:
            return()
        return next(iter(self), None), next(reversed(self), None), len(self)

    def __eq__(self, other):
        if isinstance(other, float_range) or isinstance(other, range):
            return self._attrs(self) == self._attrs(other)
        else:  # pushes __eq__ decision to other w/o inf loop
            return NotImplemented
