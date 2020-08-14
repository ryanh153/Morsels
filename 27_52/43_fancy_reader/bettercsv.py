from csv import reader
from collections import namedtuple


class FancyReader:
    def __init__(self, str_iter, fieldnames=None):
        self.reader = reader(str_iter, delimiter=',', quotechar='"')
        self.line_num = 0
        self.fieldnames = fieldnames
        self.Row = None

    def __next__(self):
        if self.Row is None:
            if self.fieldnames is None:
                self.line_num += 1
                self.fieldnames = next(self.reader)
            self.Row = namedtuple('Row', self.fieldnames)
        self.line_num += 1
        return self.Row(*next(self.reader))

    def __iter__(self):
        return self
