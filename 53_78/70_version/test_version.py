import unittest

from version import Version


class TestVersion(unittest.TestCase):

    def test_has_string_reps(self):
        version = Version('0.0.1')
        self.assertTrue(str(version) == '0.0.1')
        self.assertTrue(repr(version) == "Version('0.0.1')")

    def test_empty_version_fail(self):
        with self.assertRaises(ValueError):
            Version('')

    def test_equality(self):
        v1 = Version('1.2.0')
        self.assertTrue(v1 == v1)

        v2 = Version('2.3.4')
        self.assertFalse(v1 == v2)

        other_v1 = Version('1.2.0')
        self.assertTrue(v1 == other_v1)

        partial = Version('1.2')
        self.assertTrue(v1 == partial)

    def test_comparisons(self):
        v1p2p3 = Version('1.2.3')
        v1p3 = Version('1.3')
        v_str = '1.3'

        self.assertTrue(v1p2p3 < v1p3)
        self.assertFalse(v1p3 < v1p2p3)

        self.assertTrue(v1p2p3 <= v1p3)
        self.assertFalse(v1p3 <= v1p2p3)

        self.assertTrue(v1p3 > v1p2p3)
        self.assertFalse(v1p2p3 > v1p3)

        self.assertTrue(v1p3 >= v1p2p3)
        self.assertFalse(v1p2p3 >= v1p3)

        # Assert type errors raised with mixed types
        with self.assertRaises(TypeError):
            v1p3 < '4.0'

        with self.assertRaises(TypeError):
            v1p3 > '4.0'

        with self.assertRaises(TypeError):
            v1p3 <= '4.0'

        with self.assertRaises(TypeError):
            v1p3 >= '4.0'

        # Equal works by __str__ method existing but it shouldn't auto-fill
        self.assertFalse(v1p3 == '1.3')  # class string is actually 1.3.0


if __name__ == '__main__':
    unittest.main()
