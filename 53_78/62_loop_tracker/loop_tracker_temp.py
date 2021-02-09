class loop_tracker:
    BLANK = object()
    
    def __init__(self, iterable):
        self.iterable = iter(iterable)
        self.empty_accesses = self.size = 0
        self._cache = self._first = self._last = self.BLANK

    def __iter__(self):
        return self

    def __len__(self):
        return self.size

    def __next__(self):
        item = self._access()
        if item is self.BLANK:
            self.empty_accesses += 1
            raise StopIteration
        self.size += 1
        self._last = item
        self._cache = self.BLANK
        return item

    def _access(self):
        if self._cache is self.BLANK:
            if self._first is self.BLANK:
                self._cache = self._first = next(self.iterable, self.BLANK)
            else:
                self._cache = next(self.iterable, self.BLANK)
        return self._cache

    def is_empty(self):
        if self._access() is self.BLANK:
            return True
        return False

    @property
    def last(self):
        if self._last is self.BLANK:
            raise AttributeError(f'{self.__name__} iterator has not been accessed so it has no last attribute')
        return self._last

    @property
    def first(self):
        self._access()
        if self._first is self.BLANK:
            raise AttributeError(f'{self.__name__} iterable does not have a first attribute') from None
        return self._first
