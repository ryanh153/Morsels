from bisect import bisect_left, bisect


class SortedList:

    def __init__(self, data, key=lambda x: x):
        self.data = list(data)
        self.key_func = key
        self.data.sort(key=self.key_func)
        self.keys = [self.key_func(item) for item in self.data]

    def add(self, item):
        self.data.insert(bisect_left(self.keys, self.key_func(item)), item)
        self.keys.insert(bisect_left(self.keys, self.key_func(item)), self.key_func(item))

    def remove(self, item):
        index = bisect_left(self.keys, self.key_func(item))
        if index != self.__len__() and self.data[index] == item:
            self.data.pop(index)
            self.keys.pop(index)
        else:
            raise ValueError

    def __contains__(self, item):
        index = bisect_left(self.keys, self.key_func(item))
        return index != self.__len__() and self.data[index] == item

    def index(self, item, start=0, stop=None):
        if stop is None or stop > self.__len__():
            stop = self.__len__()
        index = bisect_left(self.keys, self.key_func(item), lo=start, hi=stop)

        if index != stop and self.data[index] == item:
            return index
        else:
            raise ValueError

    def __repr__(self):
        return f'SortedList({repr(self.data)})'

    def __iter__(self):
        return iter(self.data)

    def __next__(self):
        yield from self.data

    def __getitem__(self, index):
        return self.data.__getitem__(index)

    def __len__(self):
        return len(self.data)

    def find(self, item):
        index = bisect_left(self.keys, self.key_func(item))
        if index != self.__len__() and self.data[index] == item:
            return index
        else:
            return -1

    def rfind(self, item):
        index = bisect(self.keys, self.key_func(item))
        if self.data[index-1] == item:
            return index - 1
        else:
            return -1

    def count(self, item):
        index = bisect_left(self.keys, self.key_func(item))
        count = 0
        for val in self.data[index:]:
            if self.key_func(val) == self.key_func(item):
                if val == item:
                    count += 1
            else:
                break
        return count
