class SequenceZip:
    def __init__(self, *args):
        self.inputs = args  # store so we can reset iters when needed (enables multiple loops) and slice them
        self.iterables = [iter(i) for i in args]  # make an iterable for each argument passed
        self.length = min(len(i) for i in args)  # find the length (defined by shortest input)

    def __iter__(self):
        for _ in range(self.length):
            yield tuple(next(i) for i in self.iterables)
        self.iterables = [iter(i) for i in self.inputs]  # reset iterator

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        if isinstance(index, slice):
            return SequenceZip(*[[arg[i] for i in range(*index.indices(self.length))] for arg in self.inputs])
        elif index < 0:
            index = self.length + index
        return tuple(arg[index] for arg in self.inputs)

    def __repr__(self):
        return 'SequenceZip(' + ', '.join(repr(arg) for arg in self.inputs) + ')'

    def __eq__(self, other):
        if isinstance(other, SequenceZip):
            for self_arg, other_arg in zip(self.inputs, other.inputs):
                if self_arg[:self.length] != other_arg[:self.length]:
                    return False
            return True
        else:
            return NotImplemented
