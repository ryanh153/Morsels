from collections import UserDict
import unittest

from reprtools import format_arguments


class FormatArgumentsTests(unittest.TestCase):

    """Tests for format_arguments."""

    def test_one_positional_argument(self):
        self.assertEqual(format_arguments(1), "1")
        self.assertEqual(format_arguments(None), "None")
        self.assertEqual(format_arguments("hello"), "'hello'")

    def test_one_keyword_argument(self):
        self.assertEqual(format_arguments(n=1), "n=1")
        self.assertEqual(format_arguments(object=None), "object=None")
        self.assertEqual(format_arguments(name="Trey"), "name='Trey'")

    def test_multiple_positional_arguments(self):
        self.assertEqual(format_arguments(1, 2), "1, 2")
        self.assertEqual(
            format_arguments(" ", ["apple", "banana"]),
            "' ', ['apple', 'banana']",
        )

    def test_multiple_keyword_arguments(self):
        self.assertEqual(
            format_arguments(file="log", mode="wt"),
            "file='log', mode='wt'",
        )

    def test_mixed_arguments(self):
        self.assertEqual(
            format_arguments(["apple", "banana"], start=1),
            "['apple', 'banana'], start=1",
        )
        self.assertEqual(
            format_arguments("log", "wt", encoding="utf-8", newline=""),
            "'log', 'wt', encoding='utf-8', newline=''",
        )


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class MakeReprTests(unittest.TestCase):

    """Tests for make_repr."""

    def test_no_args_or_kwargs(self):
        from reprtools import make_repr

        class Empty:
            __repr__ = make_repr()
        self.assertEqual(str(Empty()), "Empty()")
        self.assertEqual(repr(Empty()), "Empty()")

    def test_with_args(self):
        from reprtools import make_repr

        class Point:
            def __init__(self, x, y, z):
                self.x, self.y, self.z = x, y, z
            __repr__ = make_repr(args=['x', 'y', 'z'])
        self.assertEqual(str(Point(1, 2, 3)), "Point(1, 2, 3)")
        self.assertEqual(repr(Point(x=3, y=4, z=5)), "Point(3, 4, 5)")

    def test_with_kwargs(self):
        from reprtools import make_repr

        class Point:
            def __init__(self, x, y, color="purple"):
                self.x, self.y = x, y
                self.color = color
            __repr__ = make_repr(kwargs=['x', 'y'])
        self.assertEqual(str(Point(1, 2)), "Point(x=1, y=2)")
        self.assertEqual(repr(Point(x=3, y=4)), "Point(x=3, y=4)")


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class AutoReprTests(unittest.TestCase):

    """Tests for auto_repr."""

    def test_with_args(self):
        from reprtools import auto_repr

        @auto_repr(args=['x', 'y', 'z'])
        class Point:
            def __init__(self, x, y, z):
                self.x, self.y, self.z = x, y, z
        self.assertEqual(str(Point(1, 2, 3)), "Point(1, 2, 3)")
        self.assertEqual(repr(Point(x=3, y=4, z=5)), "Point(3, 4, 5)")

    def test_with_kwargs(self):
        from reprtools import auto_repr

        @auto_repr(kwargs=['x', 'y'])
        class Point:
            def __init__(self, x, y, color="purple"):
                self.x, self.y = x, y
                self.color = color
        self.assertEqual(str(Point(1, 2)), "Point(x=1, y=2)")
        self.assertEqual(repr(Point(x=3, y=4)), "Point(x=3, y=4)")

    def test_with_inheritance(self):
        from reprtools import auto_repr

        @auto_repr(kwargs=['x', 'y', 'data'])
        class Point(UserDict):
            def __init__(self, x, y, **data):
                self.x, self.y = x, y
                super().__init__(data)
        point = Point(1, 2, color="purple")
        self.assertEqual(
            str(point),
            "Point(x=1, y=2, data={'color': 'purple'})",
        )
        self.assertEqual(list(point), ["color"])


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class auto_repr(unittest.TestCase):

    """Tests for auto_repr with no arguments."""

    def test_with_concrete_attributes_no_defaults(self):
        from reprtools import auto_repr

        @auto_repr
        class Point:
            def __init__(self, x, y, z):
                self.x, self.y, self.z = x, y, z
        self.assertEqual(str(Point(1, 2, 3)), "Point(x=1, y=2, z=3)")
        self.assertEqual(repr(Point(x=3, y=4, z=5)), "Point(x=3, y=4, z=5)")

    def test_argument_with_a_default(self):
        from reprtools import auto_repr

        @auto_repr
        class Thing:
            def __init__(self, name, color="purple"):
                self.name = name
                self.color = color
        self.assertEqual(
            str(Thing("duck")),
            "Thing(name='duck', color='purple')",
        )

    def test_with_property(self):
        from reprtools import auto_repr

        @auto_repr
        class BankAccount:

            current_id = 0

            def __init__(self, balance=0):
                self._balance = balance
                BankAccount.current_id += 1
                self.account_id = BankAccount.current_id

            @property
            def balance(self):
                return self._balance

        self.assertEqual(
            str(BankAccount()),
            "BankAccount(balance=0)",
        )
        self.assertEqual(
            str(BankAccount(5)),
            "BankAccount(balance=5)",
        )

    def test_argument_without_an_attribute(self):
        from reprtools import auto_repr

        @auto_repr
        class BankAccount:

            def __init__(self, opening_balance):
                self.balance = opening_balance

        with self.assertRaises(TypeError):
            str(BankAccount(10))

        with self.assertRaises(TypeError):
            repr(BankAccount(10))

    def test_default_argument_without_an_attribute(self):
        from reprtools import auto_repr

        @auto_repr
        class BankAccount:

            current_id = 0

            def __init__(self, balance=0, custom_id=None):
                self._balance = balance
                if not custom_id:
                    BankAccount.current_id += 1
                    custom_id = BankAccount.current_id
                self.account_id = custom_id

            @property
            def balance(self):
                return self._balance

        self.assertEqual(
            str(BankAccount(custom_id=10)),
            "BankAccount(balance=0)",
        )
        self.assertEqual(
            str(BankAccount(5)),
            "BankAccount(balance=5)",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
