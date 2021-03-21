from timeit import default_timer
import unittest

from sortedlist import SortedList


MANY_BIG_NUMBERS = list(range(50000))


class SortedListTests(unittest.TestCase):

    """Tests for SortedList."""

    def test_sorted_initializer_and_iteration(self):
        numbers = SortedList([1, 3, 4, 24, 6, 7, 23])
        self.assertEqual(list(numbers), [1, 3, 4, 6, 7, 23, 24])
        self.assertEqual(list(numbers), list(numbers))

    def test_length(self):
        numbers = SortedList([1, 3, 4, 24, 6, 7, 23])
        self.assertEqual(len(numbers), 7)

    def test_indexing(self):
        numbers = SortedList([1, 3, 4, 24, 6, 7, 23])
        self.assertEqual(numbers[1], 3)
        self.assertEqual(numbers[-1], 24)

    def test_unordered_setting_and_inserting_not_allowed(self):
        numbers = SortedList([1, 3, 4, 24, 6, 7, 23])
        self.assertEqual(numbers[1], 3)
        with self.assertRaises(Exception):
            numbers[1] = 8
        with self.assertRaises(Exception):
            numbers.insert(0, 8)
        with self.assertRaises(Exception):
            numbers.append(8)
        self.assertEqual(numbers[0], 1)
        self.assertEqual(numbers[1], 3)
        self.assertEqual(numbers[-1], 24)
        self.assertEqual(len(numbers), 7)

    def test_initializer_copies_input(self):
        input_numbers = [1, 3, 4, 24, 6, 7, 23]
        numbers = SortedList(input_numbers)
        input_numbers.append(100)
        self.assertEqual(list(numbers), [1, 3, 4, 6, 7, 23, 24])
        self.assertEqual(list(numbers), list(numbers))

    def test_string_representation(self):
        numbers = SortedList([1, 3, 4, 24, 6, 7, 23])
        self.assertEqual(repr(numbers), "SortedList([1, 3, 4, 6, 7, 23, 24])")
        self.assertEqual(str(numbers), repr(numbers))

    def test_sorted_add(self):
        numbers = SortedList([1, 3, 4, 24, 6, 7, 23])
        numbers.add(26)
        self.assertEqual(list(numbers), [1, 3, 4, 6, 7, 23, 24, 26])
        numbers.add(2)
        self.assertEqual(list(numbers), [1, 2, 3, 4, 6, 7, 23, 24, 26])

    def test_sorted_remove(self):
        numbers = SortedList([1, 3, 4, 24, 6, 7, 23])
        numbers.remove(3)
        self.assertEqual(list(numbers), [1, 4, 6, 7, 23, 24])
        with self.assertRaises(ValueError):
            numbers.remove(2)

    def test_index(self):
        numbers = SortedList([1, 3, 4, 24, 6, 7, 23])
        self.assertEqual(numbers.index(1), 0)
        self.assertEqual(numbers.index(3), 1)
        self.assertEqual(numbers.index(23), 5)
        self.assertEqual(numbers.index(4, stop=3), 2)
        self.assertEqual(numbers.index(4, stop=20), 2)
        self.assertEqual(numbers.index(23, start=4), 5)
        with self.assertRaises(ValueError):
            numbers.index(4, stop=2)
        with self.assertRaises(ValueError):
            numbers.index(23, stop=4)
        with self.assertRaises(ValueError):
            numbers.index(4, start=4)

    def test_containment(self):
        numbers = SortedList([1, 3, 4, 24, 6, 7, 23])
        self.assertTrue(1 in numbers)
        self.assertFalse(2 in numbers)
        self.assertTrue(3 in numbers)
        self.assertFalse(5 in numbers)
        self.assertTrue(23 in numbers)
        self.assertTrue(4 in numbers)
        self.assertFalse(21 in numbers)

    def test_sorting_strings(self):
        words = SortedList(['apple', 'lime', 'Lemon'])
        words.add('Banana')
        self.assertEqual(list(words), ['Banana', 'Lemon', 'apple', 'lime'])

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_find_rfind_and_count(self):
        numbers = SortedList([2, 11, 2, 1, 29, 3, 7, 4, 2, 18, 4, 2])
        self.assertEqual(numbers.find(1), 0)
        self.assertEqual(numbers.find(2), 1)
        self.assertEqual(numbers.find(3), 5)
        self.assertEqual(numbers.find(4), 6)
        self.assertEqual(numbers.find(5), -1)
        self.assertEqual(numbers.find(7), 8)
        self.assertEqual(numbers.find(100), -1)
        self.assertEqual(numbers.find(0), -1)

        self.assertEqual(numbers.count(1), 1)
        self.assertEqual(numbers.count(2), 4)
        self.assertEqual(numbers.count(3), 1)
        self.assertEqual(numbers.count(4), 2)
        self.assertEqual(numbers.count(5), 0)
        self.assertEqual(numbers.count(6), 0)
        self.assertEqual(numbers.count(7), 1)

        self.assertEqual(numbers.rfind(1), 0)
        self.assertEqual(numbers.rfind(2), 4)
        self.assertEqual(numbers.rfind(3), 5)
        self.assertEqual(numbers.rfind(4), 7)
        self.assertEqual(numbers.rfind(5), -1)
        self.assertEqual(numbers.rfind(7), 8)
        self.assertEqual(numbers.rfind(100), -1)
        self.assertEqual(numbers.rfind(0), -1)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_time_efficiency(self):
        sorted_list = SortedList(MANY_BIG_NUMBERS)
        unsorted_list = sorted(MANY_BIG_NUMBERS)
        with Timer() as sorted_add:
            sorted_list.add(0)
            sorted_list.add(20000)
            sorted_list.add(49000)
            sorted_list.add(49999)
        with Timer() as unsorted_add:
            unsorted_list.insert(unsorted_list.index(0), 0)
            unsorted_list.insert(unsorted_list.index(20000), 20000)
            unsorted_list.insert(unsorted_list.index(49000), 49000)
            unsorted_list.insert(unsorted_list.index(49999), 49999)
        self.assertLess(sorted_add.elapsed, unsorted_add.elapsed)
        with Timer() as sorted_count:
            self.assertEqual(sorted_list.count(1), 1)
            self.assertEqual(sorted_list.count(25000), 1)
            self.assertEqual(sorted_list.count(49000), 2)
            self.assertEqual(sorted_list.count(50000), 0)
        with Timer() as unsorted_count:
            self.assertEqual(unsorted_list.count(1), 1)
            self.assertEqual(unsorted_list.count(25000), 1)
            self.assertEqual(unsorted_list.count(49000), 2)
            self.assertEqual(unsorted_list.count(50000), 0)
        self.assertLess(sorted_count.elapsed, unsorted_count.elapsed)
        with Timer() as sorted_contains:
            self.assertTrue(0 in sorted_list)
            self.assertTrue(25000 in sorted_list)
            self.assertFalse(30000.5 in sorted_list)
            self.assertFalse(100000 in sorted_list)
            self.assertFalse(-1 in sorted_list)
            self.assertTrue(48000 in sorted_list)
        with Timer() as unsorted_contains:
            self.assertTrue(0 in unsorted_list)
            self.assertTrue(25000 in unsorted_list)
            self.assertFalse(30000.5 in unsorted_list)
            self.assertFalse(100000 in unsorted_list)
            self.assertFalse(-1 in unsorted_list)
            self.assertTrue(48000 in unsorted_list)
        self.assertLess(sorted_contains.elapsed, unsorted_contains.elapsed)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_key_function(self):
        words = SortedList(['apple', 'lime', 'Lemon'], key=str.lower)
        self.assertEqual(list(words), ['apple', 'Lemon', 'lime'])
        words.add('Banana')
        self.assertEqual(list(words), ['apple', 'Banana', 'Lemon', 'lime'])
        self.assertNotIn('banana', words)
        self.assertIn('Banana', words)
        self.assertEqual(words.find('banana'), -1)
        self.assertEqual(words.find('Banana'), 1)
        words.remove('Lemon')
        self.assertEqual(list(words), ['apple', 'Banana', 'lime'])
        words.add('pear')
        self.assertEqual(list(words), ['apple', 'Banana', 'lime', 'pear'])
        self.assertEqual(words.find('LIME'), -1)
        self.assertEqual(words.find('lime'), 2)
        self.assertEqual(words.rfind('LIME'), -1)
        self.assertEqual(words.rfind('lime'), 2)
        self.assertEqual(words.count('LIME'), 0)
        self.assertEqual(words.count('lime'), 1)
        words.add('LIME')
        self.assertEqual(words.count('lime'), 1)
        self.assertEqual(words.count('LIME'), 1)
        words.add('lime')
        self.assertEqual(words.count('lime'), 2)
        self.assertEqual(words.count('LIME'), 1)


class Timer:

    """Context manager to time a code block."""

    def __enter__(self):
        self.start = default_timer()
        return self

    def __exit__(self, *args):
        self.end = default_timer()
        self.elapsed = self.end - self.start


if __name__ == "__main__":
    unittest.main(verbosity=2)