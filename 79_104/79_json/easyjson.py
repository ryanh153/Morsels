import json
from types import SimpleNamespace


class DataClass:

    def __init__(self, data):
        if isinstance(data, SimpleNamespace):
            self.data = DictClass(data)
        elif isinstance(data, list):
            self.data = ListClass(data)

    def __getattr__(self, item):
        return self.data.__getattr__(item)

    __getitem__ = __getattr__

    def keys(self):
        yield from self.data.keys()

    def __eq__(self, other):
        return self.data == other

    def __repr__(self):
        return repr(self.data)


class ListClass:
    def __init__(self, data):
        self.data = data

        # Make our structure nested with instances of our data classes
        for index, entry in enumerate(self.data):
            if isinstance(entry, SimpleNamespace):
                self.data[index] = DictClass(entry)
            elif isinstance(entry, list):
                self.data[index] = ListClass(entry)

    def __getattr__(self, index):
        if index is Ellipsis:
            return self.make_stacked_data()
        return self.data[index]

    def make_stacked_data(self):
        """
        Need to take all entries and stack common keys (if entries are dict like)
        or make list of lists if (if list like).
        We do assume all entries in the list are the same type
        """
        if isinstance(self.data[0], DictClass):
            # Make a namespace that puts the values at each key across the list into a list and make DataClass instance
            stacked_data = SimpleNamespace(**{key: list() for key in self.data[0].keys()})
            for entry in self.data:
                for key in entry.keys():
                    getattr(stacked_data, key).append(entry[key])
            return DataClass(stacked_data)
        elif isinstance(self.data[0], ListClass):
            # Make a list where the 1st entry is the first value from each sublist, 2nd is the second from each, ...
            stacked_data = [list(nth_values) for nth_values in zip(*self.data)]
            return DataClass(stacked_data)

    __getitem__ = __getattr__

    def __eq__(self, other):
        if isinstance(other, list):
            return self.data == other
        return NotImplemented

    def __repr__(self):
        return '[' + ', '.join(f'{entry!r}' for entry in self.data) + ']'


class DictClass:
    def __init__(self, data):
        self.data = data

        # Make our structure nested with instances of our data classes
        for attr, value in data.__dict__.items():
            if isinstance(value, SimpleNamespace):
                setattr(self.data, attr, DictClass(value))
            elif isinstance(value, list):
                setattr(self.data, attr, ListClass(value))

    def __getattr__(self, item):
        if isinstance(item, tuple):  # Make a new data class from just the keys in the tuple
            return DataClass(
                SimpleNamespace(
                    **{attr: getattr(self, attr) for attr in item}
                )
            )
        return getattr(self.data, item)

    __getitem__ = __getattr__

    def keys(self):
        yield from self.data.__dict__

    def __eq__(self, other):
        if isinstance(other, dict):
            return dict(self) == other
        return NotImplemented

    def __repr__(self):
        return '{' + ', '.join(f'{key!r}:{value!r}' for key, value in self.data.__dict__.items()) + '}'


def parse(json_str):
    data = json.loads(json_str, object_hook=lambda d: SimpleNamespace(**d))
    return DataClass(data)
