from csv import reader


class BaseNamedList:
    __slots__ = ()

    def __init__(self, *args):
        for fn, arg in zip(self.__slots__, args):
            self.__setattr__(fn, arg)

    def __iter__(self):
        return iter([self.__getattribute__(name) for name in self.__slots__])

    def __next__(self):
        yield from [self.__getattribute__(name) for name in self.__slots__]

    def __repr__(self):
        data_str = ', '.join(f'{name}={self.__getattribute__(name)!r}' for name in self.__slots__)
        return f'{type(self).__name__}({data_str})'


def named_list_generator(typename, field_names):
    return type(typename, (BaseNamedList,), {'__slots__': tuple(field_names)})


class FancyReader:
    def __init__(self, str_iter, fieldnames=None, delimiter=',', quotechar='"'):
        self.reader = reader(str_iter, delimiter=delimiter, quotechar=quotechar)
        self.line_num = 0
        self._fieldnames = fieldnames
        self.Row = None

    def __next__(self):
        if self.Row is None:
            self.Row = named_list_generator('Row', self.fieldnames)
        self.line_num += 1
        return self.Row(*next(self.reader))

    def __iter__(self):
        return self

    @property
    def fieldnames(self):
        if self._fieldnames is None:
            self._fieldnames = next(self.reader)
            self.line_num += 1
        return self._fieldnames
