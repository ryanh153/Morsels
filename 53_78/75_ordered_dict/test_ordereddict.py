from functools import partial
from timeit import timeit
import unittest


from ordereddict import OrderedDict


class OrderedDictTests(unittest.TestCase):

    """Tests for OrderedDict."""

    def test_order_maintained(self):
        d = OrderedDict()
        pairs = [
            ('Allen', 'purple'),
            ('Kendra', 'blue'),
            ('Anita', 'green'),
            ('Wanda', 'red'),
            ('Michael', 'yellow'),
        ]
        names, colors = zip(*pairs)
        for name, color in pairs:
            d[name] = color
        self.assertEqual(tuple(d), names)
        self.assertEqual(tuple(d.keys()), names)
        self.assertEqual(tuple(d.values()), colors)
        self.assertEqual(list(d.items()), pairs)

    def test_initializer(self):
        pairs = [
            ('Allen', 'purple'),
            ('Kendra', 'blue'),
            ('Anita', 'green'),
            ('Wanda', 'red'),
            ('Michael', 'yellow'),
        ]
        d = OrderedDict(pairs)
        names, colors = zip(*pairs)
        self.assertEqual(tuple(d), names)
        self.assertEqual(tuple(d.keys()), names)
        self.assertEqual(tuple(d.values()), colors)
        self.assertEqual(list(d.items()), pairs)
        e = OrderedDict(d)
        self.assertEqual(list(e.items()), list(d.items()))

    def test_update_method(self):
        pairs = [
            ('Allen', 'purple'),
            ('Kendra', 'blue'),
            ('Anita', 'green'),
            ('Wanda', 'red'),
            ('Michael', 'yellow'),
        ]
        d = OrderedDict(pairs[:2])
        self.assertEqual(len(d), 2)
        d.update(pairs[2:])
        self.assertEqual(len(d), 5)
        names, colors = zip(*pairs)
        self.assertEqual(tuple(d), names)
        self.assertEqual(tuple(d.keys()), names)
        self.assertEqual(tuple(d.values()), colors)
        self.assertEqual(list(d.items()), pairs)

    def test_length(self):
        d = OrderedDict()
        self.assertEqual(len(d), 0)
        d['Allen'] = 'purple'
        self.assertEqual(len(d), 1)

    def test_index_method(self):
        d = OrderedDict({'Allen': 'purple'})
        pairs = [
            ('Kendra', 'blue'),
            ('Anita', 'green'),
            ('Wanda', 'red'),
            ('Michael', 'yellow'),
        ]
        names, colors = zip(*pairs)
        for name, color in pairs:
            d[name] = color
        self.assertEqual(d.index('Michael'), 4)
        self.assertEqual(d.index('Allen'), 0)
        del d['Allen']
        self.assertEqual(d.index('Michael'), 3)
        d['Allen'] = 'orange'
        self.assertEqual(d.index('Allen'), 4)
        self.assertEqual(d.index('Michael'), 3)
        self.assertEqual(d.index('Anita'), 1)
        d['Anita'] = 'grue'
        self.assertEqual(d.index('Anita'), 1)

    def test_deleting_and_reinserting_changes_order(self):
        d = OrderedDict()
        d['a'] = 3
        d['b'] = 2
        del d['a']
        self.assertEqual(list(d.items()), [('b', 2)])
        d['a'] = 1
        self.assertEqual(list(d.items()), [('b', 2), ('a', 1)])

    def test_clear(self):
        pairs = [
            ('Allen', 'purple'),
            ('Kendra', 'blue'),
            ('Anita', 'green'),
            ('Wanda', 'red'),
            ('Michael', 'yellow'),
        ]
        d = OrderedDict(pairs)
        self.assertEqual(len(d), len(pairs))
        d.clear()
        self.assertEqual(len(d), 0)

    def test_delitem(self):
        pairs = [
            ('Allen', 'purple'),
            ('Kendra', 'blue'),
            ('Anita', 'green'),
            ('Wanda', 'red'),
            ('Michael', 'yellow'),
        ]
        d = OrderedDict(pairs)
        del d['Anita']
        self.assertNotIn('Anita', d)
        with self.assertRaises(KeyError):
            del d['Anita']
        self.assertEqual(list(d.items()), pairs[:2] + pairs[3:])

    def test_setitem(self):
        pairs = [
            ('Allen', 'purple'),
            ('Kendra', 'blue'),
            ('Anita', 'green'),
            ('Wanda', 'red'),
            ('Michael', 'yellow'),
        ]
        new_pairs = [
            ('Allen', 'purple'),
            ('Kendra', 'blue'),
            ('Anita', 'green'),
            ('Wanda', 'pink'),
            ('Michael', 'yellow'),
            ('Mary', 'black'),
        ]
        d = OrderedDict(pairs)
        d['Wanda'] = 'pink'  # existing element
        d['Mary'] = 'black'  # new element
        self.assertEqual(list(d.items()), new_pairs)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_indexing_keys_and_values(self):
        pairs = [
            ('Allen', 'purple'),
            ('Kendra', 'blue'),
            ('Anita', 'green'),
            ('Wanda', 'red'),
            ('Michael', 'yellow'),
        ]
        d = OrderedDict(pairs)
        self.assertEqual(d.keys()[0], 'Allen')
        self.assertEqual(d.keys()[-1], 'Michael')
        del d['Allen']
        self.assertEqual(d.keys()[0], 'Kendra')
        d['Allen'] = 'purple'
        self.assertEqual(d.keys()[-1], 'Allen')
        d.clear()
        d.update(pairs)
        self.assertEqual(d.values()[0], 'purple')
        self.assertEqual(d.values()[-1], 'yellow')
        del d['Allen']
        self.assertEqual(d.values()[0], 'blue')
        d['Allen'] = 'purple'
        self.assertEqual(d.values()[-1], 'purple')
        self.assertFalse(
            isinstance(d.keys(), list),
            "keys() shouldn't return a list",
        )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_performance_of_indexing(self):
        d = OrderedDict()
        for n in range(10000):
            d[n] = n

        time = partial(timeit, globals=locals(), number=500)
        looping_over_everything = time("list(d)")

        # Test that index method operates in constant time
        early_key = time("d.index(0)")
        late_key = time("d.index(9999)")
        self.assertLess(late_key, early_key*100)
        self.assertLess(early_key, late_key*100)
        self.assertLess(late_key, looping_over_everything)
        self.assertLess(early_key, looping_over_everything)

        # Test that indexing keys()/values() is constant time
        early_index = time("d.keys()[0], d.values()[1]")
        late_index = time("d.keys()[9999], d.values()[-2]")
        late_index = time("d.keys()[9999], d.values()[-2]")
        self.assertLess(late_index, early_index*100)
        self.assertLess(early_index, late_index*100)
        self.assertLess(late_index, looping_over_everything*1.5)
        self.assertLess(early_index, looping_over_everything*1.5)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_key_slicing(self):
        pairs = [
            ('Allen', 'purple'),
            ('Kendra', 'blue'),
            ('Anita', 'green'),
            ('Wanda', 'red'),
            ('Michael', 'yellow'),
        ]
        d = OrderedDict(pairs)
        self.assertEqual(list(d['Kendra':'Wanda']), ['blue', 'green'])
        self.assertEqual(list(d[:'Wanda']), ['purple', 'blue', 'green'])
        self.assertEqual(list(d['Wanda':]), ['red', 'yellow'])
        self.assertEqual(list(d[:]), list(d.values()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
