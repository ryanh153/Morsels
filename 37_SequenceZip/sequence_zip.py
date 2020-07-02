class SequenceZip:
    def __init__(self, *args):
        self.inputs = args  # store so we can reset iters when needed (enables multiple loops) and slice them
        self.length = min(len(i) for i in self.inputs)  # find the length (defined by shortest input)

    def __iter__(self):
        iterables = [iter(i) for i in self.inputs]  # make iterators for each input
        yield from [tuple(next(i) for i in iterables) for _ in range(len(self))]

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        if isinstance(index, slice):
            return SequenceZip(*[[arg[i] for i in range(*index.indices(len(self)))] for arg in self.inputs])
        return tuple(arg[index] if index >= 0 else arg[len(self) + index] for arg in self.inputs)

    def __repr__(self):
        return 'SequenceZip(' + ', '.join(repr(arg) for arg in self.inputs) + ')'

    def __eq__(self, other):
        if isinstance(other, SequenceZip):
            return all(in1[:len(self)] == in2[:len(self)] for in1, in2 in zip(self.inputs, other.inputs))
        return NotImplemented
