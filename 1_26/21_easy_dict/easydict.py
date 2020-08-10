class EasyDict:
    def __init__(self, *args, **kwargs):
        self.normalize = False
        if len(kwargs):  # search for/handle normalize keyword
            if "normalize" in kwargs.keys():
                self.normalize = kwargs["normalize"]  # set normalize flag from input
                kwargs.pop("normalize")  # don't add to dict? Will it get there anyways as part of the namespace?

        if len(args):
            for arg in args:
                self.__dict__.update(arg)  # update with dicts passed
                if self.normalize:
                    for k, v in arg.items():  # also update with normed keys
                        self.__dict__[self._normalize(k)] = v
        if len(kwargs):
            self.__dict__.update(kwargs)  # update with keyword arguments
            if self.normalize:
                for k, v in kwargs.items():
                    self.__dict__[self._normalize(k)] = v

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, item):
        try:
            return self.__dict__[item]
        except KeyError:
            raise AttributeError

    def __setitem__(self, key, value):
        self.__dict__[key] = value
        if self.normalize:
            self.__dict__[self._normalize(key)] = value  # still normalize keys passed

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if self.normalize:
            self.__dict__[self._de_normalize(key)] = value  # put in de-normalized attributes

    def __eq__(self, other):
        if isinstance(other, EasyDict):
            # Each key in other is in self w/ same value
            for k, v in other.__dict__.items():
                if k in self.__dict__ and self[k] == v:
                    continue
                else:
                    return False
            # Each key in self is in other w/ same value
            for k, v in self.__dict__.items():
                if k in other.__dict__ and other[k] == v:
                    continue
                else:
                    return False
            # if so, they're the same
            return True
        return False

    def get(self, key, default=None):
        if key in self.__dict__:
            return self[key]
        else:
            return default

    @staticmethod
    def _normalize(key):
        """lower case and spaced replaced with _ to enable attribute lookup for all keys"""
        return key.lower().replace(' ', '_')

    @staticmethod
    def _de_normalize(key):
        """for attributes passed replace _ with space for key lookups"""
        return key.replace('_', ' ')
