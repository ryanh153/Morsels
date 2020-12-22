class ProxyDict:

    MISSING = object()

    def __init__(self, *input_dicts):
        self.data = [input_dict for input_dict in input_dicts[::-1]]

    def keys(self):
        yield from [key for sub_dict in self.data for key in sub_dict.keys()]

    def items(self):
        yield from [item for sub_dict in self.data for item in sub_dict.items()]

    def values(self):
        yield from [value for sub_dict in self.data for value in sub_dict.values()]

    def get(self, key, default=None):
        for sub_dict in self.data:
            if key in sub_dict:
                return sub_dict[key]
        else:
            return default

    def __getitem__(self, key):
        result = self.get(key, self.MISSING)
        if result is not self.MISSING:
            return result
        else:
            raise KeyError(f'Key: {key} is not in {type(self).__name__}')

    def __setitem__(self, key, value):
        raise TypeError(f'{type(self).__name__} does not support item assignment')

    def __eq__(self, other):
        if isinstance(other, dict):
            for key in other:
                if key not in self or self[key] != other[key]:
                    return False
            else:
                return True
        elif isinstance(other, ProxyDict):
            return self.data == other.data
        else:
            return NotImplemented

    def __len__(self):
        return sum([len(sub_dict) for sub_dict in self.data])

    def __iter__(self):
        for sub_dict in self.data:
            yield from sub_dict.keys()

    def __repr__(self):
        members = ', '.join(repr(sub_dict) for sub_dict in self.data[::-1])
        return f"{type(self).__name__}({members})"

    @property
    def maps(self):
        return [sub_dict for sub_dict in self.data[::-1]]
