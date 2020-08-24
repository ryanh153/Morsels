import math


class SliceView:

    def __init__(self, sequence, start=None, stop=None, step=1):
        self.sequence, self.step = sequence, step

        # set defaults
        if self.step > 0:
            start_def, stop_def = 0, len(sequence)
        elif self.step < 0:
            start_def, stop_def = len(sequence) - 1, -1
        else:
            raise ValueError("Step must be non-zero")

        # handle negative values
        if start is not None and start < 0:
            start = len(sequence) + start
        if stop is not None and stop < 0:
            stop = len(sequence) + stop
        # enforce defaults
        self.start = start if start is not None else start_def
        self.stop = stop if stop is not None else stop_def

        # range checks
        if self.step > 0:
            self.start = max([0, self.start])
            self.stop = min([len(sequence), self.stop])
        elif self.step < 0:
            self.start = min([len(sequence) - 1, self.start])
            self.stop = max([-1, self.stop])

        self.index = self.start

    def __next__(self):
        if (self.step > 0 and self.index < self.stop) or (self.index > self.stop):
            result = self.sequence[self.index]
            self.index += self.step
            return result
        else:
            self.index = self.start
            raise StopIteration

    def __iter__(self):
        return self

    def __len__(self):
        return math.ceil(abs((self.start-self.stop)/self.step))

    def __getitem__(self, index):
        if isinstance(index, slice):
            new_step = index.step if index.step is not None else 1
            return SliceView(self.sequence, index.start, index.stop, new_step)
        elif index >= 0:
            return self.sequence[self.start + self.step * index]
        else:
            return self.sequence[self.start + self.step * (len(self) + index)]
