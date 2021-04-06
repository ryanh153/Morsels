from collections import ChainMap
from collections.abc import Mapping


class ProxyDict(Mapping):

    def __init__(self, *input_dicts):
        self.data = ChainMap(*input_dicts[::-1])

    def __getitem__(self, key):
        return self.data[key]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        yield from self.data.keys()

    def __repr__(self):
        members = ', '.join(repr(my_map) for my_map in self.data.maps[::-1])
        return f"{type(self).__name__}({members})"

    @property
    def maps(self):
        return self.data.maps[::-1]
