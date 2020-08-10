from itertools import cycle
import math


class CyclicList:
    def __init__(self, iterable):
        # Get two iterables from input. First will never be incremented so we can reset to start when we need to
        self._iterable = iterable  # remember original so we can spawn new instances of our CyclicList
        self.iterable = cycle(iterable)

    def __next__(self):
        return next(self.iterable)

    def __iter__(self):
        return CyclicList(self._iterable)  # return a new cyclic list (not our own iterator) when asked for an iterator

    def __len__(self):
        return len(self._iterable)

    def append(self, item):
        self._iterable.append(item)

    def pop(self, index=None):
        if index is None:
            return self._iterable.pop()
        elif isinstance(index, int):
            return self._iterable.pop(index)

    def _convert_index(self, index):
        if index >= 0:
            return index % self.__len__()
        else:
            return index + math.floor(abs(index)/self.__len__())*self.__len__()

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop = index.start, index.stop
            if start is None:
                start = 0
            if stop is None:
                stop = self.__len__() if start >= 0 else 0
            return [self._iterable[self._convert_index(i)] for i in range(start, stop)]
        else:
            return self._iterable[self._convert_index(index)]

    def __delitem__(self, index):
        self._iterable.pop(self._convert_index(index))

    def __setitem__(self, index, value):
        self._iterable[self._convert_index(index)] = value
