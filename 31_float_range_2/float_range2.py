class float_range:

    def __init__(self, *args):
        if len(args) == 3:  # passed all arguments
            self.start, self.stop, self.step = args
        elif len(args) == 2:  # passed start/stop
            self.start, self.stop, self.step = *args, 1
        elif len(args) == 1:  # passed stop
            self.start, self.stop, self.step = 0, *args, 1
        else:
            raise TypeError("float_range expected 1, 2 or 3 arguments. Got 0 or more than 3.")

        self.steps = 0
        self._list = [self.start + self.step*i for i in range(len(self))]

    def __len__(self):
        steps = int((self.stop-self.start)/self.step)
        if self.start + self.step*steps != self.stop:
            steps += 1  # does not hit end, so we do return the last element before stop is passed
        return max([0, steps])

    def __iter__(self):
        return self

    def __next__(self):
        if self.steps == len(self):
            self.steps = 0
            raise StopIteration
        else:
            self.steps += 1
            return self.start + self.step*(self.steps-1)

    def __getitem__(self, my_slice):
        return self._list[my_slice]

    def __reversed__(self):
        start = self._list[-1]
        step = -1 * self.step
        stop = self._list[0] + 0.5*step  # need to include the last item in the stored list
        return float_range(start, stop+0.5*step, step)
