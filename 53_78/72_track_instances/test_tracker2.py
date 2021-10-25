import unittest


from tracker2 import track_instances


class TrackInstancesDecoratorTests(unittest.TestCase):

    """Tests for track_instances."""

    def test_bank_account(self):
        @track_instances
        class BankAccount:
            def __init__(self, balance=0):
                self.balance = balance
            def __repr__(self):
                return "BankAccount({})".format(self.balance)
        account1 = BankAccount(5)
        self.assertEqual(set(BankAccount.instances), {account1})
        account2 = BankAccount(10)
        self.assertEqual(set(BankAccount.instances), {account1, account2})

    def test_works_with_inheritance(self):
        class Animal:
            def __init__(self, name):
                self.name = name
            def __repr__(self):
                return "{}({})".format(repr(self.name))
        @track_instances
        class Squirrel(Animal):
            def __init__(self, name, nervousness=0.99):
                self.nervousness = nervousness
                super().__init__(name)
        squirrel1 = Squirrel(name='Mike')
        squirrel2 = Squirrel(name='Carol', nervousness=0.5)
        self.assertEqual(squirrel1.name, 'Mike')
        self.assertEqual(squirrel2.name, 'Carol')
        self.assertEqual(squirrel1.nervousness, 0.99)
        self.assertEqual(squirrel2.nervousness, 0.5)
        self.assertEqual(set(Squirrel.instances), {squirrel1, squirrel2})

    def test_usage_on_two_classes_is_independent(self):
        @track_instances
        class A:
            pass
        @track_instances
        class B:
            def __init__(self, x):
                self.x = x
                super().__init__()
        a = A()
        self.assertEqual(set(A.instances), {a})
        b = B(3)
        self.assertEqual(set(B.instances), {b})
        self.assertEqual(set(A.instances), {a})
        self.assertEqual(a.instances, A.instances)
        self.assertEqual(b.instances, B.instances)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_deleted_instances_are_not_maintained(self):
        @track_instances
        class A:
            def __init__(self, name):
                self.name = name
            def __repr__(self):
                return "A({})".format(repr(self.name))
        x = A('x')
        self.assertEqual(set(A.instances), {x})
        y = A('y')
        self.assertEqual(set(A.instances), {x, y})
        del x
        self.assertEqual(set(A.instances), {y})
        z = A('z')
        self.assertEqual(set(A.instances), {y, z})

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_accepts_attribute_name_argument(self):
        @track_instances('instances')
        class A:
            pass
        x = A()
        self.assertEqual(set(A.instances), {x})
        y = A()
        self.assertEqual(set(A.instances), {x, y})

        @track_instances('_registry')
        class B:
            def __init__(self, x):
                self.x = x
        b = B(3)
        self.assertEqual(set(B._registry), {b})
        c = B(4)
        self.assertEqual(set(B._registry), {b, c})
        self.assertEqual(b._registry, B._registry)
        with self.assertRaises(AttributeError):
            A._registry

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_iterating_over_class(self):
        from tracker2 import InstanceTracker
        class Animal:
            def __init__(self, name):
                self.name = name
        class Squirrel(Animal, metaclass=InstanceTracker):
            def __init__(self, name, nervousness=0.99):
                self.nervousness = nervousness
                super().__init__(name)
        squirrel1 = Squirrel(name='Mike')
        squirrel2 = Squirrel(name='Carol', nervousness=0.5)
        self.assertEqual(squirrel1.name, 'Mike')
        self.assertEqual(squirrel2.name, 'Carol')
        self.assertEqual(squirrel1.nervousness, 0.99)
        self.assertEqual(squirrel2.nervousness, 0.5)
        self.assertEqual(set(Squirrel), {squirrel1, squirrel2})


if __name__ == "__main__":
    unittest.main(verbosity=2)