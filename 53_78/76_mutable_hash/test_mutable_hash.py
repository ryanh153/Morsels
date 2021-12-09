import unittest


from mutable_hash import mutable_hash


class MutableHashTests(unittest.TestCase):

    """Tests for mutable_hash."""

    def test_hashing_lists(self):
        self.assertEqual(mutable_hash([1, 2, 3]), mutable_hash([1, 2, 3]))
        self.assertNotEqual(mutable_hash([1, 2, 3]), mutable_hash([1, 2, 4]))
        self.assertNotEqual(mutable_hash([1, 2, 3]), mutable_hash([3, 2, 1]))
        self.assertNotEqual(
            mutable_hash([1, 2, 3]),
            mutable_hash([1, 2, 3, 4]),
        )
        self.assertEqual(mutable_hash([5.6, 7.8]), mutable_hash([5.6, 7.8]))
        big_list1 = list(range(10000))
        big_list2 = big_list1.copy()
        self.assertEqual(mutable_hash(big_list1), mutable_hash(big_list2))
        self.assertNotEqual(
            mutable_hash(big_list1),
            mutable_hash(big_list2[::-1]),
        )
        big_list2[-1], big_list2[-2] = big_list2[-2], big_list2[-1]
        self.assertNotEqual(mutable_hash(big_list1), mutable_hash(big_list2))

    def test_hashing_sets(self):
        colors1 = {'red', 'purple'}
        colors2 = {'red', 'purple'}
        self.assertEqual(mutable_hash(colors1), mutable_hash(colors2))
        self.assertEqual(mutable_hash({1, 2, 3}), mutable_hash({1, 2, 3}))
        self.assertNotEqual(mutable_hash({1, 2, 3}), mutable_hash({1, 2, 4}))
        big_set1 = set(str(i) for i in reversed(range(1000)))
        big_set2 = set(str(i) for i in range(1000))
        self.assertEqual(mutable_hash(big_set1), mutable_hash(big_set2))

    def test_hashing_dictionaries(self):
        colors = {
            'red': 1,
            'blue': 4,
            'green': 3,
        }
        colors2 = colors.copy()
        self.assertEqual(mutable_hash(colors), mutable_hash(colors))
        self.assertEqual(mutable_hash(colors), mutable_hash(colors2))
        colors2['green'] = 2
        self.assertNotEqual(mutable_hash(colors), mutable_hash(colors2))
        colors2.update({'green': 4, 'blue': 3})
        self.assertNotEqual(mutable_hash(colors), mutable_hash(colors2))
        self.assertEqual(
            mutable_hash({1: 2, 3: 4}),
            mutable_hash({3: 4, 1: 2}),
        )

    def test_hashing_immutable_types(self):
        self.assertEqual(mutable_hash('hello'), hash('hello'))
        self.assertEqual(mutable_hash(2), hash(2))
        self.assertEqual(mutable_hash(2.5), hash(2.5))
        self.assertEqual(mutable_hash((1, 2)), mutable_hash((1, 2)))
        self.assertEqual(
            mutable_hash(frozenset({2, 3})),
            hash(frozenset({2, 3})),
        )

    def test_hashing_unknown_unhashable_type(self):
        class Point:
            def __init__(self, x, y):
                self.x, self.y = x, y
            def __eq__(self, other):
                (self.x, self.y) == (other.x, other.y)
        p = Point(1, 2)
        with self.assertRaises(TypeError):
            mutable_hash(p)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_hashwrapper(self):
        from mutable_hash import HashWrapper, UnsafeDict
        my_list = [1, 2, 3]
        wrapper = HashWrapper(my_list)
        self.assertEqual(hash(wrapper), mutable_hash(my_list))
        self.assertEqual(wrapper, my_list)
        self.assertEqual(wrapper, [1, 2, 3])
        values = [
            ['red', 'pink'],
            ['blue', 'purple'],
            ['green', 'mauve'],
            ['pink', 'red'],
            ['blue', 'purple'],
        ]
        counts = UnsafeDict()
        for item in values:
            counts.setdefault(item, 0)
            counts[item] += 1
        self.assertEqual(counts[values[0]], 1)
        self.assertEqual(counts[values[1]], 2)
        self.assertEqual(counts[values[2]], 1)
        self.assertEqual(len(counts), 4)
        self.assertEqual(counts.pop(values[0]), 1)
        self.assertEqual(len(counts), 3)
        self.assertTrue(values[1] in counts)
        counts.clear()
        self.assertEqual(len(counts), 0)
        self.assertEqual(repr(UnsafeDict([(['k'], ['v'])])), "{['k']: ['v']}")

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_deep_mutable_hashing(self):
        # Test tuple of lists
        self.assertEqual(
            mutable_hash(([1, 2, 3], [4, 5, 6])),
            mutable_hash(([1, 2, 3], [4, 5, 6])),
        )
        self.assertNotEqual(
            mutable_hash(([1, 2, 3], [4, 5, 6])),
            mutable_hash(([1, 2, 3], [4, 100, 6])),
        )
        # Test dict-of-dicts with inner dict having list values
        self.assertEqual(
            mutable_hash({True: {(1, 2): ['red']}, False: {(1, 2): ['blue']}}),
            mutable_hash({True: {(1, 2): ['red']}, False: {(1, 2): ['blue']}}),
        )
        self.assertNotEqual(
            mutable_hash({True: {(1, 3): ['red']}, False: {(1, 2): ['blue']}}),
            mutable_hash({True: {(1, 2): ['red']}, False: {(1, 2): ['blue']}}),
        )
        self.assertNotEqual(
            mutable_hash({True: {(1, 2): ['red']}, False: {(1, 2): ['red']}}),
            mutable_hash({True: {(1, 2): ['red']}, False: {(1, 2): ['blue']}}),
        )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_registering_new_types(self):
        class Point:
            def __init__(self, x, y):
                self.x, self.y = x, y
            def __eq__(self, other):
                (self.x, self.y) == (other.x, other.y)
        @mutable_hash.register(Point)
        def point_hash(point):
            return hash((point.x, point.y))
        self.assertEqual(
            mutable_hash(Point(1, 2)),
            mutable_hash(Point(1, 2)),
        )
        self.assertNotEqual(
            mutable_hash(Point(1, 2)),
            mutable_hash(Point(1, 3)),
        )
        self.assertNotEqual(
            mutable_hash(Point(1, 2)),
            mutable_hash(Point(2, 1)),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)