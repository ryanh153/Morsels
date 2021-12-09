from collections import UserDict


def hashable(value):
    return getattr(value, '__hash__') is not None


class mutable_hash:
    """
    Gross way to make it so we can register types and functions for our mutable hash function
    """

    registered_types = dict()

    def __new__(cls, data):
        return cls._mutable_hash(data)

    @classmethod
    def register(cls, data_type):
        def decorator(func):
            cls.registered_types[data_type] = func

            def inner(*args, **kwargs):
                return func(*args, **kwargs)
            return inner

        return decorator

    @classmethod
    def _mutable_hash(cls, data):
        """
            Hash an object (mutable or not)
            :param data:
                if data is
                - a registered type : Return that types corresponding has function
                - hashable : return the objects hash
                - list : Hash where order and value matters
                - set : Hash where only values matters
                - dict : Hash where we care about which key, value pairs are in the dictionary but not their order
            :return:
                Hash of the object as defined above.
            """
        for registered_type, registered_function in cls.registered_types.items():
            if isinstance(data, registered_type):
                return registered_function(data)
        if hashable(data):
            if hasattr(data, '__getitem__') and any([not hashable(value) for value in data]):
                return hash(tuple([value if hashable(value) else mutable_hash(value) for value in data]))
            return hash(data)
        if isinstance(data, list):
            return hash(tuple(data))
        if isinstance(data, set):
            return sum([hash(val) for val in data])
        if isinstance(data, dict):
            return sum([mutable_hash(item) for item in data.items()])
        raise TypeError(f'Data type {type(data)} is not implemented yet')


class HashWrapper:

    def __init__(self, data):
        self.data = data

    def __hash__(self):
        return mutable_hash(self.data)

    def __eq__(self, other):
        if isinstance(other, HashWrapper):
            return hash(self) == hash(other)
        return hash(self) == mutable_hash(other)


class UnsafeDict(UserDict):

    def __init__(self, *args, **kwargs):
        self.actual_keys = list()
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        self.actual_keys.append(key)
        self.data[mutable_hash(key)] = value

    def __getitem__(self, key):
        return self.data[mutable_hash(key)]

    def __delitem__(self, key):
        del self.actual_keys[self.actual_keys.index(key)]
        del self.data[mutable_hash(key)]

    def __contains__(self, item):
        return super().__contains__(mutable_hash(item))

    def clear(self) -> None:
        self.actual_keys = list()
        self.data = dict()

    def values(self):
        for key in self.actual_keys:
            yield self.data[mutable_hash(key)]

    def __repr__(self):
        return ', '.join([f'{{{key!r}: {value!r}}}' for key, value in zip(self.actual_keys, self.values())])
