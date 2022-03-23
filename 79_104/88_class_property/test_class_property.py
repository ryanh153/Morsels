import unittest


from class_property import class_property


class ClassPropertyTests(unittest.TestCase):

    """Tests for class_property."""

    def test_accessing_attribute(self):
        class BankAccount:
            accounts = []
            def __init__(self, balance=0):
                self.balance = balance
                self.accounts.append(self)
            @class_property
            def total_balance(cls):
                return sum(a.balance for a in cls.accounts)
        account1 = BankAccount(5)
        account2 = BankAccount(15)
        self.assertEqual(BankAccount.total_balance, 20)
        self.assertEqual(account1.total_balance, 20)
        self.assertEqual(account1.total_balance, account2.total_balance)

    def test_first_argument_is_class_itself(self):
        class Thing:
            @class_property
            def stuff(cls):
                self.assertIs(cls, Thing)
                return cls
        self.assertIs(Thing.stuff, Thing)
        self.assertIs(Thing().stuff, Thing)

    def test_same_name_as_instance_attribute(self):
        class BankAccount:
            accounts = []
            def __init__(self, balance=0):
                self.balance = balance
                self.accounts.append(self)
            @class_property
            def total_balance(cls):
                return sum(a.balance for a in cls.accounts)
        account1 = BankAccount(5)
        account2 = BankAccount(15)
        account1.total_balance = 30
        self.assertEqual(BankAccount.total_balance, 20)
        self.assertEqual(account1.total_balance, 30)
        self.assertEqual(account2.total_balance, 20)
        del account1.total_balance
        self.assertEqual(account1.total_balance, 20)
        with self.assertRaises(AttributeError):
            del account1.total_balance


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class ClassOnlyPropertyTests(unittest.TestCase):

    """Tests for class_only_property."""

    def test_accessing_attribute_on_class(self):
        from class_property import class_only_property
        class BankAccount:
            accounts = []
            def __init__(self, balance=0):
                self.balance = balance
                self.accounts.append(self)
            @class_only_property
            def total_balance(cls):
                return sum(a.balance for a in cls.accounts)
        BankAccount(5)
        BankAccount(15)
        self.assertEqual(BankAccount.total_balance, 20)

    def test_accessing_attribute_on_instances(self):
        from class_property import class_only_property
        class BankAccount:
            accounts = []
            def __init__(self, balance=0):
                self.balance = balance
                self.accounts.append(self)
            @class_only_property
            def total_balance(cls):
                return sum(a.balance for a in cls.accounts)
        account1 = BankAccount(5)
        account2 = BankAccount(15)
        with self.assertRaises(AttributeError):
            account1.total_balance
            account2.total_balance
        self.assertEqual(BankAccount.total_balance, 20)

    def test_first_argument_is_class_itself(self):
        from class_property import class_only_property
        class Thing:
            @class_only_property
            def stuff(cls):
                self.assertIs(cls, Thing)
                return cls
        self.assertIs(Thing.stuff, Thing)


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class MoreClassOnlyPropertyTests(unittest.TestCase):

    def test_shadowing_attribute_name_on_instances(self):
        from class_property import class_only_property

        # Same-named attribute on instance
        class BankAccount:
            accounts = []
            def __init__(self, balance=0):
                self.balance = balance
                self.accounts.append(self)
            @class_only_property
            def balance(cls):
                return sum(a.balance for a in cls.accounts)
        account1 = BankAccount(5)
        account2 = BankAccount(15)
        self.assertEqual(account1.balance, 5)
        self.assertEqual(account2.balance, 15)
        self.assertEqual(BankAccount.balance, 20)

        # Setting attribute on instance
        from class_property import class_only_property
        class BankAccount:
            accounts = []
            def __init__(self, balance=0):
                self.balance = balance
                self.accounts.append(self)
            @class_only_property
            def total_balance(cls):
                return sum(a.balance for a in cls.accounts)
        account1 = BankAccount(5)
        account2 = BankAccount(15)
        account1.total_balance = 10
        account2.total_balance = 15
        self.assertEqual(BankAccount.total_balance, 20)
        self.assertEqual(account1.total_balance, 10)
        self.assertEqual(account2.total_balance, 15)


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class ClassOnlyMethodTests(unittest.TestCase):

    """Tests for class_only_method."""

    def test_calling_method_on_class(self):
        from class_property import class_only_method
        class BankAccount:
            accounts = []
            def __init__(self, balance=0):
                self.balance = balance
                self.accounts.append(self)
            @class_only_method
            def total(cls):
                return sum(a.balance for a in cls.accounts)
        BankAccount(5)
        BankAccount(15)
        self.assertEqual(BankAccount.total(), 20)

    def test_calling_method_on_instance(self):
        from class_property import class_only_method
        class BankAccount:
            accounts = []
            def __init__(self, balance=0):
                self.balance = balance
                self.accounts.append(self)
            @class_only_method
            def total(cls):
                return sum(a.balance for a in cls.accounts)
        account1 = BankAccount(5)
        account2 = BankAccount(15)
        with self.assertRaises(AttributeError):
            account1.total()
            account2.total()

    def test_first_argument_is_class_itself(self):
        from class_property import class_only_method
        class Thing:
            @class_only_method
            def stuff(cls):
                self.assertIs(cls, Thing)
                return cls
        self.assertIs(Thing.stuff(), Thing)

    def test_passing_arguments(self):
        from class_property import class_only_method
        class Thing:
            @class_only_method
            def stuff(cls, a, b):
                self.assertIs(cls, Thing)
                return (a, b)
        self.assertEqual(Thing.stuff(3, b=4), (3, 4))

    def test_method_name(self):
        from class_property import class_only_method
        class Thing:
            @class_only_method
            def stuff(cls, a, b):
                self.assertIs(cls, Thing)
                return (a, b)
        self.assertIn('stuff', repr(Thing.stuff))

    def test_documentation(self):
        from class_property import class_only_method
        class Thing:
            @class_only_method
            def stuff(cls, a, b):
                """Do things."""
                self.assertIs(cls, Thing)
                return (a, b)
        self.assertIsNotNone(Thing.stuff.__doc__)
        self.assertIn('Do things', Thing.stuff.__doc__)

    def test_same_name_as_instance_attribute(self):
        from class_property import class_only_method
        class BankAccount:
            accounts = []
            def __init__(self, balance=0):
                self.balance = balance
                self.accounts.append(self)
            @class_only_method
            def total(cls):
                return sum(a.balance for a in cls.accounts)
        account1 = BankAccount(5)
        account2 = BankAccount(15)
        account1.total = 30
        self.assertEqual(BankAccount.total(), 20)
        self.assertEqual(account1.total, 30)
        with self.assertRaises(AttributeError):
            del account2.total


if __name__ == "__main__":
    unittest.main(verbosity=2)