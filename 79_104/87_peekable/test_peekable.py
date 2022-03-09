import unittest
from itertools import islice

from peekable import peekable


class PeekableTests(unittest.TestCase):

    """Tests for peekable."""

    def assertIterableEqual(self, iterable1, iterable2):
        self.assertEqual(list(iterable1), list(iterable2))

    def test_stop_iteration_with_empty_sequence(self):
        iterator = peekable(iter([]))
        with self.assertRaises(StopIteration):
            iterator.peek()
        self.assertIterableEqual(iterator, [])
        with self.assertRaises(StopIteration):
            iterator.peek()
        self.assertIterableEqual(iterator, [])

    def test_single_None_value(self):
        iterator = peekable(iter([None]))
        self.assertEqual(iterator.peek(), None)
        self.assertIterableEqual(iterator, [None])
        with self.assertRaises(StopIteration):
            iterator.peek()
        self.assertIterableEqual(iterator, [])

    def test_peeked_item_is_cached(self):
        iterator = peekable(n**2 for n in [1, 2, 3, 4, 5])
        self.assertEqual(iterator.peek(), 1)
        self.assertIterableEqual(islice(iterator, 2), [1, 4])
        self.assertEqual(iterator.peek(), 9)
        self.assertEqual(iterator.peek(), 9)
        self.assertIterableEqual(islice(iterator, 2), [9, 16])
        self.assertIterableEqual(islice(iterator, 2), [25])
        with self.assertRaises(StopIteration):
            iterator.peek()
        self.assertIterableEqual(iterator, [])

    def test_default_value_to_peek(self):
        iterator = peekable(n**2 for n in [1, 2, 3])
        self.assertEqual(iterator.peek(default=0), 1)
        self.assertIterableEqual(iterator, [1, 4, 9])
        self.assertIsNone(iterator.peek(default=None))
        self.assertEqual(iterator.peek(default=1), 1)
        self.assertEqual(iterator.peek(default=[]), [])
        self.assertEqual(iterator.peek(default=()), ())
        self.assertEqual(iterator.peek(default=''), '')

    def test_non_iterator(self):
        iterator = peekable([1, 2, 3])
        self.assertEqual(iterator.peek(), 1)
        self.assertIterableEqual(islice(iterator, 2), [1, 2])
        self.assertEqual(iterator.peek(), 3)
        self.assertIterableEqual(iterator, [3])
        with self.assertRaises(StopIteration):
            iterator.peek()

    def test_does_not_exhaust_iterator(self):
        squares = (n**2 for n in [1, 2, 3])
        iterator = peekable(squares)
        self.assertEqual(next(squares), 1)
        self.assertEqual(iterator.peek(), 4)
        self.assertEqual(next(iterator), 4)
        self.assertEqual(next(squares), 9)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_truthiness(self):
        # no peeking
        iterator = peekable(iter(['a', 'b', '']))
        self.assertTrue(iterator)
        self.assertIs(bool(iterator), True)
        self.assertEqual(next(iterator), 'a')
        self.assertTrue(iterator)
        self.assertEqual(next(iterator), 'b')
        self.assertTrue(iterator)
        self.assertEqual(next(iterator), '')
        self.assertFalse(iterator)
        self.assertIs(bool(iterator), False)

        # peek first
        iterator = peekable(iter(['a', 'b', 'c']))
        self.assertEqual(next(iterator), 'a')
        self.assertEqual(next(iterator), 'b')
        self.assertEqual(iterator.peek(), 'c')
        self.assertTrue(iterator)
        self.assertEqual(next(iterator), 'c')
        self.assertFalse(iterator)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_prepend(self):
        iterator = peekable(iter(['a', 'b', 'c']))

        # prepend and next
        self.assertEqual(next(iterator), 'a')
        iterator.prepend('d')
        self.assertEqual(next(iterator), 'd')

        # prepend and peek
        iterator.prepend('e')
        self.assertEqual(iterator.peek(), 'e')
        self.assertEqual(next(iterator), 'e')

        # peek and prepend twice and peek
        self.assertEqual(iterator.peek(), 'b')
        iterator.prepend('f')
        iterator.prepend('g')
        self.assertEqual(iterator.peek(), 'g')
        self.assertEqual(next(iterator), 'g')
        self.assertEqual(next(iterator), 'f')
        self.assertEqual(next(iterator), 'b')

        # prepend just before end
        iterator.prepend('h')
        iterator.prepend('i')
        iterator.prepend('j')
        self.assertEqual(next(iterator), 'j')
        self.assertEqual(next(iterator), 'i')
        self.assertEqual(next(iterator), 'h')
        self.assertEqual(next(iterator), 'c')

        # prepend after end
        self.assertEqual(iterator.peek(default='z'), 'z')
        iterator.prepend('k')
        self.assertEqual(iterator.peek(default='z'), 'k')
        self.assertEqual(next(iterator), 'k')
        with self.assertRaises(StopIteration):
            next(iterator)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_supports_positive_indexing_and_slicing(self):
        iterator = peekable(iter(['a', 'b', 'c', 'd', 'e']))
        self.assertEqual(iterator[:2], ['a', 'b'])
        self.assertEqual(iterator[0], 'a')
        self.assertEqual(iterator[2], 'c')
        self.assertEqual(next(iterator), 'a')
        self.assertEqual(next(iterator), 'b')
        self.assertEqual(next(iterator), 'c')
        self.assertEqual(iterator[0], 'd')
        self.assertEqual(next(iterator), 'd')
        self.assertEqual(next(iterator), 'e')
        self.assertEqual(iterator[:2], [])


class AllowUnexpectedSuccessRunner(unittest.TextTestRunner):
    """Custom test runner to avoid FAILED message on unexpected successes."""
    class resultclass(unittest.TextTestResult):
        def wasSuccessful(self):
            return not (self.failures or self.errors)


if __name__ == "__main__":
    from platform import python_version
    import sys
    if sys.version_info < (3, 6):
        sys.exit("Running {}.  Python 3.6 required.".format(python_version()))
    unittest.main(verbosity=2, testRunner=AllowUnexpectedSuccessRunner)
