from collections import UserString


class MutableString(UserString, str):

    def __init__(self, seq):
        self._data = [c for c in seq]

    def __setitem__(self, index, value):
        self._data[index] = value

    @property
    def data(self):
        return "".join(self._data)

    @data.setter
    def data(self, value):
        self._data = value

    # TODO: Could we just delete a value in _data?
    def __delitem__(self, index):
        lst = [c for c in self.data]
        del lst[index]
        self._data = lst

    def append(self, value):
        self._data.extend(value)

    def insert(self, index, value):
        lst = [c for c in self._data]
        lst.insert(index, value)
        self._data = lst

    def pop(self, index=-1):
        popped = self._data[index]
        lst = [c for c in self._data]
        del lst[index]
        self._data = lst
        return MutableString(popped)

    def __iadd__(self, other):
        if isinstance(other, str):
            self._data.extend(c for c in other)
        elif isinstance(other, MutableString):
            self._data.extend(c for c in other.data)
        else:
            return NotImplemented
        return self

    def __imul__(self, other):
        if isinstance(other, int):
            self._data[:] = self._data*other
        else:
            return NotImplemented
        return self

    def __ne__(self, other):
        return not self.__eq__(other)
