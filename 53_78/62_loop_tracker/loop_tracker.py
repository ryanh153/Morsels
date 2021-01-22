from itertools import tee


BLANK = object()


class loop_tracker:

    def __init__(self, iterable):
        self.iterable, temp = tee(iter(iterable), 2)
        self.empty_accesses = 0
        self.total_accesses = 0
        try:
            self.first = next(temp)
        except StopIteration:
            pass
        self.next = BLANK
        self._last = BLANK

    def __next__(self):
        self.total_accesses += 1
        if self.next is not BLANK:
            self._last = self.next
            self.next = BLANK
            return self.last

        try:
            self._last = next(self.iterable)
            return self._last
        except StopIteration:
            self.empty_accesses += 1
            raise StopIteration

    def __iter__(self):
        return self

    def __len__(self):
        return self.total_accesses - self.empty_accesses

    def is_empty(self):
        try:
            self.next = next(self.iterable)
            return False
        except StopIteration:
            return True

    @property
    def last(self):
        if self._last is BLANK:
            raise AttributeError(f'{self.__name__} iterator has not been accessed so it has no last attribute')
        return self._last
