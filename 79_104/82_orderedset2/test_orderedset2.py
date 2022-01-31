from collections.abc import Mapping, Iterable
from functools import partial
from sys import getsizeof
from textwrap import dedent
from timeit import timeit

import unittest


from orderedset2 import OrderedSet


class OrderedSetTests(unittest.TestCase):

    """Tests for OrderedSet."""

    def test_constructor_with_iterables(self):
        OrderedSet([1, 2, 3, 4])
        OrderedSet(n**2 for n in [1, 2, 3])

    def test_constructor_with_nothing(self):
        OrderedSet()

    def test_string_representations(self):
        numbers = OrderedSet(n**2 for n in [1, 2, 3, 4])
        empty = OrderedSet()
        self.assertEqual(str(numbers), "OrderedSet([1, 4, 9, 16])")
        self.assertEqual(repr(empty), "OrderedSet([])")

    def test_iterable(self):
        numbers = OrderedSet([1, 2, 3, 4])
        self.assertEqual(set(numbers), {1, 2, 3, 4})

    def test_uniqueness(self):
        numbers = OrderedSet([1, 3, 2, 4, 2, 1, 4, 5])
        self.assertEqual(sorted(numbers), [1, 2, 3, 4, 5])

    def test_maintains_order_and_uniqueness(self):
        string = "Hello world.  This string contains many characters in it."
        expected = "Helo wrd.Thistngcamy"
        characters = OrderedSet(string)
        self.assertEqual("".join(characters), expected)

    def test_length(self):
        numbers = OrderedSet([1, 2, 4, 2, 1, 4, 5])
        self.assertEqual(len(numbers), 4)
        self.assertEqual(len(OrderedSet('hiya')), 4)
        self.assertEqual(len(OrderedSet('hello there')), 7)

    def test_containment(self):
        numbers = OrderedSet([1, 2, 4, 2, 1, 4, 5])
        self.assertIn(2, numbers)
        self.assertNotIn(3, numbers)

    def test_memory_and_time_efficient(self):
        # Time efficient construction
        time = partial(timeit, globals=globals(), number=75)
        small_set_time = time("OrderedSet([9999 for _ in range(1000)])")
        large_set_time = time("OrderedSet([9999 + i for i in range(1000)])")
        self.assertGreater(small_set_time*100, large_set_time)

        # Memory efficient
        numbers = OrderedSet([9999 for _ in range(2500)])
        numbers2 = OrderedSet([9999 + i for i in range(2500)])
        self.assertLess(get_size(numbers)*10, get_size(numbers2))
        self.assertLess(get_size(numbers), 3000)

        # Time efficient lookups
        first = next(iter(numbers2))
        time = partial(timeit, globals=locals(), number=2000)
        beginning_lookup = time("assert first in numbers2")
        not_in_lookup = time("assert 13000 not in numbers2")
        self.assertGreater(beginning_lookup*350, not_in_lookup)

    def test_add_and_discard(self):
        numbers = OrderedSet([1, 2, 3])
        numbers.add(3)
        self.assertEqual(len(numbers), 3)
        numbers.add(4)
        self.assertEqual(len(numbers), 4)
        numbers.discard(4)
        self.assertEqual(len(numbers), 3)
        numbers.discard(4)
        self.assertEqual(len(numbers), 3)

        # Make sure the add method is efficient too!
        setup = "numbers = OrderedSet([])"
        time = partial(timeit, setup=setup, globals=globals(), number=100)
        small_set_time = time(dedent("""
            add = numbers.add
            for n in [9999 for _ in range(1000)]:
                add(n)
        """))
        large_set_time = time(dedent("""
            add = numbers.add
            for n in [9999 + i for i in range(1000)]:
                add(n)
        """))
        self.assertGreater(small_set_time*30, large_set_time)

    def test_equality(self):
        self.assertEqual(OrderedSet('abc'), OrderedSet('abc'))
        self.assertNotEqual(OrderedSet('abc'), OrderedSet('bac'))
        self.assertEqual(OrderedSet('abc'), set('abc'))
        self.assertEqual(OrderedSet('bac'), set('abc'))
        self.assertNotEqual(OrderedSet('abc'), 'abc')
        self.assertNotEqual(OrderedSet('abc'), ['a', 'b', 'c'])
        numbers = OrderedSet([1, 2, 3])
        numbers2 = OrderedSet([1, 2, 3, 4])
        self.assertNotEqual(numbers, numbers2)
        self.assertFalse(numbers == numbers2)
        numbers.add(4)
        self.assertEqual(numbers, numbers2)
        self.assertFalse(numbers != numbers2)

    def test_indexing_and_reversed(self):
        string = "Hello world.  This string contains many characters in it."
        expected = "Helo wrd.Thistngcamy"
        characters = OrderedSet(string)
        self.assertEqual(characters[0], 'H')
        self.assertEqual(characters[2], 'l')
        self.assertEqual(characters[3], 'o')
        self.assertEqual(characters[-1], 'y')
        self.assertEqual(list(reversed(characters)), list(expected[::-1]))

        # Test time efficiency of indexing
        numbers = OrderedSet(9999 for _ in range(50000))
        numbers2 = OrderedSet(9999 + i for i in range(50000))
        time = partial(timeit, globals=locals(), number=25)
        small_set_time = time("numbers[len(numbers)//2]")
        large_set_time = time("numbers2[len(numbers2)//2]")
        self.assertGreater(small_set_time*500, large_set_time)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_set_like_behaviors(self):
        string1 = "The five boxing wizards jump quickly."
        string2 = "Hi there"
        characters1 = OrderedSet(string1)
        characters2 = OrderedSet(string2)
        self.assertEqual(
            characters1 - characters2,
            OrderedSet("Tfvboxngwzadsjumpquckly."),
        )
        self.assertEqual(
            characters2 - characters1,
            OrderedSet("Ht"),
        )
        self.assertEqual(
            characters1 | characters2,
            OrderedSet("The fivboxngwzardsjumpquckly.Ht"),
        )
        self.assertEqual(
            characters2 | characters1,
            OrderedSet("Hi therTfvboxngwzadsjumpquckly."),
        )
        self.assertEqual(
            characters1 & characters2,
            OrderedSet("he ir"),
        )
        self.assertEqual(
            characters2 & characters1,
            OrderedSet("i her"),
        )
        self.assertEqual(
            characters1 ^ characters2,
            OrderedSet("Tfvboxngwzadsjumpquckly.Ht"),
        )
        self.assertEqual(
            characters2 ^ characters1,
            OrderedSet("HtTfvboxngwzadsjumpquckly."),
        )
        characters = characters1
        self.assertEqual(characters1, OrderedSet(string1))
        self.assertIs(characters, characters1)
        characters1 -= OrderedSet("abc 123")
        self.assertEqual(
            "".join(characters1),
            "Thefivoxngwzrdsjumpqkly.",
        )
        self.assertIs(characters, characters1)
        characters1 &= OrderedSet("Who are you?")
        self.assertEqual(
            "".join(characters1),
            "heoruy",
        )
        self.assertIs(characters, characters1)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_count_remove_and_append(self):
        numbers = OrderedSet([1, 2, 3])
        self.assertEqual(numbers.count(2), 1)
        numbers.remove(2)
        self.assertEqual(numbers.count(2), 0)
        self.assertEqual(list(numbers), [1, 3])
        self.assertIn(3, numbers)
        numbers.remove(3)
        self.assertNotIn(3, numbers)
        self.assertEqual(list(numbers), [1])
        self.assertNotIn(2, numbers)
        numbers.append(2)
        self.assertIn(2, numbers)
        self.assertEqual(list(numbers), [1, 2])
        with self.assertRaises(ValueError):
            numbers.append(2)
        self.assertEqual(list(numbers), [1, 2])
        with self.assertRaises(ValueError):
            numbers.append(1)
        numbers.remove(1)
        self.assertEqual(list(numbers), [2])
        numbers.append(1)
        self.assertEqual(list(numbers), [2, 1])
        with self.assertRaises(ValueError):
            numbers.append(1)
        with self.assertRaises(ValueError):
            numbers.remove(9)
        with self.assertRaises(KeyError):
            numbers.remove(9)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_index_setting_deleting_pop(self):
        numbers = OrderedSet([1, 2, 3])
        self.assertEqual(numbers.index(2), 1)
        self.assertEqual(numbers.index(1), 0)
        self.assertEqual(numbers.index(3), 2)
        with self.assertRaises(ValueError):
            numbers.index(4)
        numbers.remove(2)
        with self.assertRaises(ValueError):
            numbers.index(2)
        numbers.append(2)
        self.assertEqual(list(numbers), [1, 3, 2])
        self.assertIn(1, numbers)
        self.assertNotIn(8, numbers)
        numbers[0] = 8
        self.assertNotIn(1, numbers)
        self.assertIn(8, numbers)
        self.assertEqual(list(numbers), [8, 3, 2])
        numbers.append(9)
        self.assertEqual(list(numbers), [8, 3, 2, 9])
        self.assertIn(9, numbers)
        del numbers[-1]
        self.assertNotIn(9, numbers)
        self.assertEqual(list(numbers), [8, 3, 2])
        self.assertIn(8, numbers)
        self.assertEqual(numbers.pop(0), 8)
        self.assertNotIn(8, numbers)
        self.assertEqual(list(numbers), [3, 2])
        numbers.append(10)
        numbers.append(11)
        self.assertEqual(list(numbers), [3, 2, 10, 11])
        numbers[-2] = 9
        self.assertEqual(list(numbers), [3, 2, 9, 11])
        numbers[-2] = 9
        self.assertEqual(list(numbers), [3, 2, 9, 11])
        with self.assertRaises(ValueError):
            numbers[-1] = 9
        self.assertEqual(list(numbers), [3, 2, 9, 11])
        with self.assertRaises(ValueError):
            numbers[0] = 2
        self.assertEqual(list(numbers), [3, 2, 9, 11])
        numbers[0] = 4
        self.assertEqual(list(numbers), [4, 2, 9, 11])
        self.assertEqual(numbers.pop(), 11)
        self.assertEqual(numbers.pop(), 9)


def get_size(obj, seen=None):
    """Return size of any Python object."""
    if seen is None:
        seen = set()
    size = getsizeof(obj)
    if id(obj) in seen:
        return 0
    seen.add(id(obj))
    if hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    if hasattr(obj, '__slots__'):
        size += sum(
            get_size(getattr(obj, attr), seen)
            for attr in obj.__slots__
            if hasattr(obj, attr)
        )
    if isinstance(obj, Mapping):
        size += sum(
            get_size(k, seen) + get_size(v, seen)
            for k, v in obj.items()
        )
    elif isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
        size += sum(get_size(item, seen) for item in obj)
    return size


if __name__ == "__main__":
    unittest.main(verbosity=2)
