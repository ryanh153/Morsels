from csv import reader


def namedlist(typename, field_names):
    def __init__(self, *args):
        for fn, arg in zip(field_names, args):
            self.__setattr__(fn, arg)

    def __iter__(self):
        return iter([self.__getattribute__(name) for name in self.__slots__])

    def __next__(self):
        yield from [self.__getattribute__(name) for name in self.__slots__]

    def __repr__(self):
        data_str = ', '.join([f'{name}={self.__getattribute__(name)!r}' for name in self.__slots__])
        return f'{typename}({data_str})'

    class_namespace = {'__slots__': tuple(fn for fn in field_names),
                       '__init__': __init__,
                       '__iter__': __iter__,
                       '__next__': __next__,
                       '__repr__': __repr__,
                       }
    result = type(typename, (), class_namespace)
    return result


class FancyReader:
    def __init__(self, str_iter, fieldnames=None, delimiter=',', quotechar='"'):
        self.reader = reader(str_iter, delimiter=delimiter, quotechar=quotechar)
        self.line_num = 0
        self._fieldnames = fieldnames
        self.Row = None

    def __next__(self):
        if self.Row is None:
            self.Row = namedlist('Row', self.fieldnames)
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
