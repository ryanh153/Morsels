import unittest
import easyjson
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

class ParseTests(unittest.TestCase):

    """Tests for parse."""

    def test_dictionary_key_syntax(self):
        data = easyjson.parse("""{
            "user": "Trey",
            "is active": true,
            "numbers": [1, 2, 3]
        }""")
        self.assertEqual(data['user'], "Trey")
        self.assertIs(data['is active'], True)
        self.assertEqual(data['numbers'], [1, 2, 3])

    def test_attribute_syntax(self):
        data = easyjson.parse("""{
            "user": "Trey",
            "is_active": true,
            "numbers": [1, 2, 3]
        }""")
        self.assertEqual(data.user, "Trey")
        self.assertEqual(data.numbers, [1, 2, 3])

    def test_deep_objects(self):
        data = easyjson.parse("""{
            "user": "Trey",
            "colors": {
                "red": true,
                "green": false,
                "blue": true
            }
        }""")
        self.assertIs(data.colors.red, True)
        self.assertIs(data.colors.green, False)
        self.assertIs(data.colors.blue, True)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_repr_equality_and_dict_conversion(self):
        data = easyjson.parse("""{
            "user": "Trey",
            "numbers": [1, 2, 3],
            "colors": {
                "red": true,
                "green": false,
                "blue": true
            }
        }""")
        self.assertEqual(
            data.colors,
            {'red': True, 'green': False, 'blue': True},
        )
        self.assertEqual(eval(repr(data)), data)
        self.assertEqual(
            dict(data.colors),
            {'red': True, 'green': False, 'blue': True},
        )
        self.assertEqual(set({**data}), {"user", "numbers", "colors"})

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_tuples_as_keys(self):
        data = easyjson.parse("""{
            "user": "Trey",
            "numbers": [1, 2, 3],
            "colors": {
                "red": true,
                "green": false,
                "blue": true
            }
        }""")
        self.assertEqual(
            data['user', 'numbers'],
            {'user': 'Trey', 'numbers': [1, 2, 3]},
        )
        self.assertEqual(data['user', 'colors'].colors.red, True)
        self.assertEqual(
            data.colors['red', 'blue'],
            {'red': True, 'blue': True},
        )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_querying_arrays(self):
        # Querying objects in an array
        data = easyjson.parse("""[{
            "id": 1,
            "user": "Robert"
        }, {
            "id": 2,
            "user": "Cheryl"
        }, {
            "id": 3,
            "user": "Linda"
        }]""")
        self.assertEqual(list(data[...]['id']), [1, 2, 3])
        self.assertEqual(list(data[...].user), ["Robert", "Cheryl", "Linda"])

        # Querying array of arrays
        data = easyjson.parse("""[
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]""")
        self.assertEqual(list(data[...][0]), [1, 4, 7])
        self.assertEqual(list(data[...][2]), [3, 6, 9])

        # Only queries one level deep
        data = easyjson.parse("""{
            "result": {
                "users": [{
                    "id": 4,
                    "profile": {"id": 16, "name": "Mildred"}
                }, {
                    "id": 6,
                    "profile": {"id": 18, "name": "James"}
                }, {
                    "id": 5,
                    "profile": {"id": 17, "name": "Gloria"}
                }, {
                    "id": 3,
                    "profile": {"id": 15, "name": "William"}
                }]
            }
        }""")
        users = data.result.users
        self.assertEqual(list(users[...].id), [4, 6, 5, 3])
        self.assertEqual(users[...].profile[2], {"id": 17, "name": "Gloria"})
        self.assertEqual(users[...].profile[0]['name'], "Mildred")
        self.assertEqual(users[...].profile[1].id, 18)
        self.assertEqual(list(users[...].profile[...].id), [16, 18, 17, 15])


if __name__ == "__main__":
    unittest.main(verbosity=2)