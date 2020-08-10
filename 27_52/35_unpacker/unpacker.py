class Unpacker:

    def __init__(self, user_dict=None):
        self.__dict__ = dict(user_dict) if user_dict is not None else {}

    def __getitem__(self, item):  # and takes from it as well
        if isinstance(item, tuple):
            return tuple(self.__dict__[key] for key in item)
        else:
            return self.__dict__[item]

    def __setitem__(self, key, value):  # user updates their data dict and it's reflected in class attributes
        if isinstance(key, tuple):
            values = tuple(value)
            if len(key) == len(values):
                self.__dict__.update(zip(key, values))
            else:
                raise ValueError(f'key and value tuples in setitem are not the same length!')
        else:
            self.__dict__[key] = value

    def __iter__(self):
        yield from self.__dict__.values()  # iterable that goes through user's data

    def __repr__(self):
        attrs = ', '.join(f'{key}={repr(val)}' for key, val in self.__dict__.items())
        return f'Unpacker({attrs})'
