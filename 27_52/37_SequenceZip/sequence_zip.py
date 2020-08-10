from collections.abc import Sequence


class SequenceZip(Sequence):
    """Like built in zip but handles sequences only so we can index it.
    Inherit from sequence for type checking."""

    def __init__(self, *sequences):
        self.sequences = sequences

    def __len__(self):
        """Length by shortest. Do every time since we don't copy the sequences"""
        return min(len(seq) for seq in self.sequences)

    def __getitem__(self, index):
        """Implement indexing and slicing for our sequences.
        Get iteration for free since we have __getitem___ and __len__"""
        if isinstance(index, slice):
            return SequenceZip(*[[seq[i] for i in range(*index.indices(len(self)))] for seq in self.sequences])
        return tuple(arg[index] if index >= 0 else arg[len(self) + index] for arg in self.sequences)

    def __repr__(self):
        return f'{type(self).__name__}(' + ', '.join(repr(arg) for arg in self.sequences) + ')'

    def __eq__(self, other):
        if not isinstance(other, SequenceZip):
            return NotImplemented
        return tuple(seq[:len(self)] for seq in self.sequences) == tuple(seq[:len(self)] for seq in other.sequences)
