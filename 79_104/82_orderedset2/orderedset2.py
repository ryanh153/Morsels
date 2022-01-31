from itertools import chain


class OrderedSet:

    def __new__(cls, value=None):
        if isinstance(value, cls):
            return value
        return super().__new__(cls)

    def __init__(self, entries=None):
        self.set, self.list = set(), list()
        if entries is not None:
            for entry in entries:
                self.add(entry)

    def __len__(self):
        return len(self.set)

    def __getitem__(self, index):
        return self.list[index]

    def __setitem__(self, index, value):
        if value in self and self[index] != value:
            raise ValueError(f'{value} is already in {self!r}')
        self.set.remove(self.list[index])
        self.set.add(value)
        self.list[index] = value

    def __delitem__(self, index):
        self.set.remove(self.list[index])
        del self.list[index]

    def __repr__(self):
        return f'OrderedSet([' + ', '.join([repr(entry) for entry in self.list]) + '])'

    def __iter__(self):
        yield from self.list

    def __contains__(self, item):
        return item in self.set

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return self.list == other.list
        elif isinstance(other, set):
            return self.set == other
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, OrderedSet):
            return OrderedSet([val for val in self.list if val not in other.set])
        return NotImplemented

    def __isub__(self, other):
        for entry in other:
            self.discard(entry)
        return self

    def __or__(self, other):
        if isinstance(other, OrderedSet):
            data = list()
            for entry in chain(self, other):
                if entry not in data:
                    data.append(entry)
            return OrderedSet(data)
        return NotImplemented

    def __and__(self, other):
        if isinstance(other, OrderedSet):
            return OrderedSet([val for val in self if val in other])
        return NotImplemented

    def __iand__(self, other):
        mask = [(val in other, val) for val in self]
        for flag, entry in mask:
            if not flag:
                self.discard(entry)
        return self

    def __xor__(self, other):
        if isinstance(other, OrderedSet):
            return OrderedSet([val for val in self if val not in other] + [val for val in other if val not in self])
        return NotImplemented

    def add(self, entry):
        if entry not in self.set:
            self.set.add(entry)
            self.list.append(entry)

    def discard(self, entry):
        if entry in self.set:
            self.set.remove(entry)
            self.list.remove(entry)

    def count(self, entry):
        return int(entry in self)

    def append(self, entry):
        if entry in self:
            raise ValueError(f'{entry} already in {self}')
        self.add(entry)

    def remove(self, entry):
        if entry not in self:
            raise MyError(f'Cannot remove {entry}. Not in {self}')
        self.discard(entry)

    def index(self, entry):
        return self.list.index(entry)

    def pop(self, index=-1):
        value = self[index]
        self.discard(self[index])
        return value


class MyError(KeyError, ValueError):
    pass
