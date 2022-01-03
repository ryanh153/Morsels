from collections import UserDict, UserList, defaultdict

import json


class BiDict(UserDict):
    """Dictionary that allows look up by key or value
    Note: Currently you can't add any items in the __init__ function"""

    def __init__(self):
        self.by_key = dict()
        self.by_value = dict()
        super().__init__(self)

    def __setitem__(self, key, value):
        if isinstance(value, dict):  # Need to create a new bi-directional dictionary and nest
            self.by_key[key] = self.add_sub_dict(value)
        else:  # Just add the value to by_key and the key to by_value for lookup
            self.by_key[key] = value
            if hasattr(value, '__hash__') and getattr(value, '__hash__') is not None:
                self.by_value[value] = key

    @staticmethod
    def add_sub_dict(normal_dict):
        """
        Our dictionary contains dictionaries that we also want to be bi-direction. Go deeper.
        :param normal_dict:
            The normal dictionary pulled we want to make bi-directional
        :return:
            A new instance of ourself from the dictionary
        """
        bi_dict = BiDict()
        for sub_key, sub_value in normal_dict.items():
            bi_dict[sub_key] = sub_value
        return bi_dict

    def __getitem__(self, key):
        if isinstance(key, tuple):  # Multiple keys passed as tuple
            return self.get_multiple_keys(key)
        if key in self.by_key:  # Check if we are given a key
            return self.by_key[key]
        else:  # Otherwise assume it's a value and look it up in that dictionary
            return self.by_value[key]

    def get_multiple_keys(self, keys):
        """
        From a tuple of multiple keys make a new instance of ourself from the values at those keys
        :param keys:
            Tuple of keys to get data from
        :return:
            A new BiDict instance with just the requested keys
        """
        bi_dict = BiDict()
        for sub_key in keys:
            bi_dict[sub_key] = self.by_key[sub_key]
        return bi_dict

    __getattr__ = __getitem__

    def __repr__(self):
        return '{' + ', '.join(f'{key!r}:{value!r}' for key, value in self.by_key.items()) + '}'

    def __eq__(self, other):
        if isinstance(other, dict):
            return all([self[key] == other[key] for key in self])
        return NotImplemented

    def __iter__(self):
        yield from (key for key in self.by_key)

    def __contains__(self, item):
        return item in list(self.keys())


class JsonList(UserList):
    """
    This is a data structure designed to hold instances of BiDict.
    The idea is that a json structure can have a list of the same keys in each entry and we need to represent that.
    """

    def __init__(self):
        super().__init__()

    def append(self, item):
        self.data.append(item)

    def __getitem__(self, item):
        if item is Ellipsis:  # Need to return a structure that will look for a key in all entries
            temp = BiDict()
            for bi_dict in self.data:
                for key, value in bi_dict.by_key.items():
                    if key not in temp:
                        temp[key] = list()
                    temp[key].append(value)
            return temp
        else:  # Just passed key. Look for it in the top level
            return self.data[0][item]

    __getattr__ = __getitem__

    def keys(self):
        """This is needed to make dictionary unpacking (**self) work"""
        yield from (key for key in self.data[0].by_key)

    def __repr__(self):
        result = self.data[0].__repr__()
        return result

    def __eq__(self, other):
        return self.data[0] == other


def parse(json_str: str) -> BiDict:
    """
    Parse a string with json formatting into a dictionary with key and value look up. This look up is enabled for top
    level and all sub levels that are dictionary objects when using json.load
    :param json_str:
        The string version of the json file
    :return:
        A bi-directional dictionary that can have other bi-directional dictionaries as values.
    """
    parsed = json.loads(json_str)
    if not isinstance(parsed,  list):
        parsed = [parsed]

    j_list = JsonList()
    for entry in parsed:
        bi_dict = BiDict()
        for key, value in entry.items():
            bi_dict[key] = value
        j_list.append(bi_dict)
    return j_list


# data = parse("""{
#             "user": "Trey",
#             "numbers": [1, 2, 3],
#             "colors": {
#                 "red": true,
#                 "green": false,
#                 "blue": true
#             }
#         }""")
#
# print(data)
# print(data.colors)
# print(dict(data.colors))
