from collections.abc import Sequence


class ChainSequence:
    def __init__(self, *sequences):
        self.sequences = [seq for seq in sequences]
        self.major_index, self.minor_index = 0, 0

    def __getitem__(self, index):
        if isinstance(index, slice):
            return SliceView(self, index.start, index.stop, index.step)
        if index < 0:
            index += len(self)

        if index < 0 or index >= len(self):
            raise IndexError(f'Index {index} out of bounds for {type(self).__name__} with length {len(self)}')

        for seq in self.sequences:
            if index >= len(seq):
                index -= len(seq)
            else:
                return seq[index]

    def __len__(self):
        return sum(len(s) for s in self.sequences)

    def __repr__(self):
        return f'{type(self).__name__}(' + ', '.join(repr(seq) for seq in self.sequences) + ')'

    def __add__(self, other):
        if isinstance(other, Sequence):
            return ChainSequence(*self.sequences, other)
        return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Sequence):
            self.sequences.append(other)
            return self
        return NotImplemented


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
