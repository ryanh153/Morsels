class float_range:

    def __init__(self, start, stop=None, step=1):
        if stop is None:
            start, stop = 0, start
        self.start, self.stop, self.step = start, stop, step
        self._calculate_length()

    def _calculate_length(self):
        self._len = int((self.stop - self.start) / self.step)
        if self.start + self.step * self._len != self.stop:
            self._len += 1  # does not hit end, so we do return the last element before stop is passed
        self._len = max([0, self._len])

    def __len__(self):
        return self._len

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            new_start = self.start + start*self.step
            new_stop = self.start + stop*self.step
            new_step = step*self.step
            return float_range(new_start, new_stop, new_step)
        if 0 <= index < len(self):
            return self.start + self.step*index
        elif 0 > index >= -1*len(self):
            return self.start + self.step*(len(self)+index)
        else:
            raise IndexError("Index is out of range")
