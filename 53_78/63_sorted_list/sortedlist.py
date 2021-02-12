from bisect import bisect_left, bisect, insort
import sys


class SortedList:

    def __init__(self, data, key=lambda x: x):
        self.key = key
        self.data = sorted(((key(d), d) for d in data))

    def _entry(self, item):
        return self.key(item), item

    def add(self, item):
        insort(self.data, self._entry(item))

    def remove(self, item):
        del self.data[self.index(item)]

    def index(self, item, start=0, stop=sys.maxsize):
        stop = min(stop, self.__len__())
        index = bisect_left(self.data, self._entry(item), lo=start, hi=stop)
        if index != stop and self.data[index] == self._entry(item):
            return index
        raise ValueError

    def __contains__(self, item):
        index = bisect_left(self.data, self._entry(item))
        return index != self.__len__() and self.data[index] == self._entry(item)

    def __repr__(self):
        return f'{type(self).__name__}({repr([d for k, d in self.data])})'

    def __getitem__(self, index):
        return self.data.__getitem__(index)[1]

    def __len__(self):
        return len(self.data)

    def find(self, item):
        index = bisect_left(self.data, self._entry(item))
        return index if index != len(self) and self.data[index] == self._entry(item) else -1

    def rfind(self, item):
        index = bisect(self.data, self._entry(item))
        return index-1 if self.data[index-1] == self._entry(item) else -1

    def count(self, item):
        index_left = bisect_left(self.data, self._entry(item))
        index_right = bisect(self.data, self._entry(item))
        return index_right - index_left
