class SliceView:

    def __init__(self, sequence, start=None, stop=None, step=None):
        start, stop, step = slice(start, stop, step).indices(len(sequence))
        self.range = range(start, stop, step)
        self.sequence = sequence

    def __iter__(self):
        yield from [self.sequence[i] for i in self.range]

    def __len__(self):
        return len(self.range)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return SliceView(list(self), index.start, index.stop, index.step)
        return self.sequence[self.range[index]]
