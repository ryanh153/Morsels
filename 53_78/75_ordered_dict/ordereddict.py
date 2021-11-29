from collections import OrderedDict as BaseDict


class OrderedDict(BaseDict):

    def __init__(self, *args, **kwargs):
        """An ordered dictionary that supports a variety of extra index based features"""
        # Set up an index dictionary where we store the position each key was inserted
        self.indices = {}
        # Set up lazy but indexable key/value data
        self._keys = IndexableLazyIterable()
        self._values = IndexableLazyIterable()
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        """Slice through keys if key is a slice. Otherwise do normal dictionary lookup"""
        if isinstance(key, slice):
            start = self.indices[key.start] if key.start is not None else 0
            stop = self.indices[key.stop] if key.stop is not None else len(self)
            return [self[self.keys()[index]] for index in range(start, stop)]
        else:
            return super().__getitem__(key)

    def __setitem__(self, key, value):
        # Track all new keys added in our indices dictionary
        if key not in self.indices:
            index = len(self)
            self.indices[key] = index
            # Add them to our key/value iterables (stored by key to make indexable)
            self._keys[index] = key
            self._values[index] = value
        super().__setitem__(key, value)

    def __delitem__(self, delete_key):
        # Decrement all indices after the key we're deleting
        delete_index = self.indices[delete_key]
        for key, index in self.indices.items():
            if index > delete_index:
                self.indices[key] -= 1

        # Remove the key from indices dictionary as well as key/value stores
        del self.indices[delete_key]
        del self._keys[delete_index]
        del self._values[delete_index]

        super().__delitem__(delete_key)

    def clear(self):
        self.indices = dict()
        self._keys = IndexableLazyIterable()
        self._values = IndexableLazyIterable()
        super().clear()

    def index(self, search_key):
        return self.indices[search_key]

    @property
    def keys(self):
        return self._keys

    @property
    def values(self):
        return self._values


class IndexableLazyIterable:
    def __init__(self):
        self.indices_dict = {}

    def __setitem__(self, key, value):
        self.indices_dict[key] = value

    def __delitem__(self, delete_key):
        for key, value in self.indices_dict.items():
            # Point everything past the delete key to the data in front of it
            if delete_key <= key < len(self.indices_dict) - 1:
                self.indices_dict[key] = self.indices_dict[key + 1]
        # Remove the last now that we have reordered
        else:
            del self.indices_dict[key]

    def __iter__(self):
        yield from self.indices_dict.values()

    def __getitem__(self, index):
        if index < 0:
            index += len(self.indices_dict)
        return self.indices_dict[index]

    def __call__(self):
        return self
