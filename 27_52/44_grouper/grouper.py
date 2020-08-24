from collections import UserDict, defaultdict, Mapping


class Grouper(UserDict):

    def __init__(self, iterable=None, key=None):
        self.data, self.key = defaultdict(list), key
        self.update(iterable)

    def update(self, new_data):
        if isinstance(new_data, Mapping):
            for key, values in new_data.items():
                self.data[key].extend(values)
        elif new_data is not None:
            for item in new_data:
                self.data[self.key(item)].append(item)

    def add(self, item):
        self.data[self.key(item)].append(item)

    def group_for(self, item):
        return self.key(item)

    def __add__(self, other):
        if not isinstance(other, Grouper):
            return NotImplemented
        elif self.key != other.key:
            raise ValueError("Cannot add Groupers with different key functions")
        new_group = type(self)(self, self.key)
        new_group.update(other.data)
        return new_group
