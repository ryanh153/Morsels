from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
import unittest
import warnings

from warningutils import error_on_warnings


class ErrorOnWarningsTests(unittest.TestCase):

    """Tests for error_on_warnings"""

    def setUp(self):
        warnings.resetwarnings()

    def tearDown(self):
        warnings.resetwarnings()

    def test_every_warning_raises_exceptions(self):
        with redirect_stderr(StringIO()) as output:
            with error_on_warnings():
                with self.assertRaises(UserWarning):
                    warnings.warn('A generic warning')
                with self.assertRaises(DeprecationWarning):
                    warnings.warn('A deprecation warning', DeprecationWarning)
            self.assertEqual(output.getvalue(), "")
            warnings.warn('A generic warning')
            warnings.warn('A deprecation warning', DeprecationWarning)
            self.assertIn('A generic warning', output.getvalue())
            self.assertIn('A deprecation warning', output.getvalue())

    def test_specific_categories_raise_exceptions(self):
        class MyFancyDeprecation(DeprecationWarning):
            """A custom deprecation warning."""
        with redirect_stderr(StringIO()) as output:
            with error_on_warnings(category=DeprecationWarning):
                warnings.warn('A generic warning')
                with self.assertRaises(DeprecationWarning):
                    warnings.warn('A deprecation warning', DeprecationWarning)
                with self.assertRaises(MyFancyDeprecation):
                    warnings.warn('Another warning', MyFancyDeprecation)
                warnings.warn('A second generic warning', ImportWarning)
            with error_on_warnings(category=Warning):
                with self.assertRaises(UserWarning):
                    warnings.warn('A different generic warning')
            self.assertIn('A generic warning', output.getvalue())
            self.assertIn('A second generic warning', output.getvalue())
            self.assertNotIn('A different generic warning', output.getvalue())

    def test_specific_warning_messages(self):
        with redirect_stderr(StringIO()) as output:
            with error_on_warnings('.*deprecation'):
                warnings.warn('One')
                warnings.warn('Two', DeprecationWarning)
                warnings.warn('Three', ImportWarning)
                with self.assertRaises(DeprecationWarning):
                    warnings.warn('A deprecation warning', DeprecationWarning)
                with self.assertRaises(DeprecationWarning):
                    warnings.warn('A Deprecation warning', DeprecationWarning)
            self.assertIn('One', output.getvalue())
            self.assertIn('Two', output.getvalue())
            self.assertIn('Three', output.getvalue())
            with error_on_warnings('deprecation'):
                warnings.warn('A deprecation warning', DeprecationWarning)
            self.assertIn('A deprecation warning', output.getvalue())
            with error_on_warnings('.*generic'):
                warnings.warn('A deprecation warning', DeprecationWarning)
                with self.assertRaises(UserWarning):
                    warnings.warn('First generic warning')
                with self.assertRaises(ImportWarning):
                    warnings.warn('Second generic warning', ImportWarning)
            self.assertIn('A deprecation warning', output.getvalue())
            self.assertNotIn('generic warning', output.getvalue())

    def test_category_and_message(self):
        class MyFancyDeprecation(DeprecationWarning):
            """A custom deprecation warning."""
        with redirect_stderr(StringIO()) as output:
            with error_on_warnings(category=DeprecationWarning):
                warnings.warn('generic warning 1')
                with self.assertRaises(DeprecationWarning):
                    warnings.warn('A deprecation warning', DeprecationWarning)
                with self.assertRaises(MyFancyDeprecation):
                    warnings.warn('Another warning', MyFancyDeprecation)
                warnings.warn('generic warning 2', ImportWarning)
            with error_on_warnings(category=Warning):
                with self.assertRaises(UserWarning):
                    warnings.warn('generic warning 3')
            warnings.warn('generic warning 4', ImportWarning)
        self.assertIn('generic warning 1', output.getvalue())
        self.assertIn('generic warning 2', output.getvalue())
        self.assertNotIn('generic warning 3', output.getvalue())
        self.assertIn('generic warning 4', output.getvalue())

    def test_resets_filters_properly(self):
        with redirect_stderr(StringIO()) as output:
            warnings.simplefilter('error', ResourceWarning)
            with error_on_warnings():
                with self.assertRaises(UserWarning):
                    warnings.warn('error1')
            with self.assertRaises(Exception):
                warnings.warn('error2', category=ResourceWarning)
            warnings.warn('error3')
        self.assertNotIn('error1', output.getvalue())
        self.assertNotIn('error2', output.getvalue())
        self.assertIn('error3', output.getvalue())

    def test_nesting_context_managers(self):
        with redirect_stderr(StringIO()) as output:
            with error_on_warnings(category=UserWarning):
                with error_on_warnings(category=ResourceWarning):
                    with self.assertRaises(Exception):
                        warnings.warn('warning1')
                    with self.assertRaises(Exception):
                        warnings.warn('warning2', ResourceWarning)
                    warnings.warn('warning3', DeprecationWarning)
                warnings.warn('warning4', ResourceWarning)
                with self.assertRaises(Exception):
                    warnings.warn('warning5')
            warnings.warn('warning6')
            warnings.warn('warning7', ResourceWarning)
        self.assertNotIn('warning1', output.getvalue())
        self.assertNotIn('warning2', output.getvalue())
        self.assertIn('warning3', output.getvalue())
        self.assertIn('warning4', output.getvalue())
        self.assertNotIn('warning5', output.getvalue())
        self.assertIn('warning6', output.getvalue())
        self.assertIn('warning7', output.getvalue())

    # To test the Bonus part of this exercise, comment out the following line
    @unittest.expectedFailure
    def test_using_as_a_decorator(self):
        with redirect_stderr(StringIO()) as output:
            @error_on_warnings(category=DeprecationWarning)
            def make_resource_warning():
                warnings.warn('Resource error', ResourceWarning)

            @error_on_warnings(category=DeprecationWarning)
            def make_deprecation_warning():
                warnings.warn('Deprecation error', DeprecationWarning)
            make_resource_warning()
            self.assertIn('Resource error', output.getvalue())
            with self.assertRaises(DeprecationWarning):
                make_deprecation_warning()
            self.assertNotIn('Deprecation error', output.getvalue())


# To test the Bonus part of this exercise, comment out the following line
@unittest.expectedFailure
class CaptureWarningsTests(unittest.TestCase):

    """Tests for capture_warnings"""

    def setUp(self):
        warnings.resetwarnings()

    def tearDown(self):
        warnings.resetwarnings()

    def test_catch_all_warnings(self):
        from warningutils import capture_warnings
        with redirect_stdout(StringIO()) as output:
            with redirect_stderr(output):
                with capture_warnings():
                    warnings.warn('A generic warning')
                    warnings.warn('A deprecation warning', DeprecationWarning)
                self.assertEqual(output.getvalue(), '')
                warnings.warn('A generic warning')
                warnings.warn('A deprecation warning', DeprecationWarning)
                self.assertNotEqual(output.getvalue(), '')

    def test_capture_warnings_into_list(self):
        from warningutils import capture_warnings
        with capture_warnings() as caught:
            warnings.warn('A generic warning')
            self.assertEqual(len(caught), 1)
            warnings.warn('A deprecation warning', DeprecationWarning)
            self.assertEqual(len(caught), 2)
        self.assertEqual(caught[0].message.args, ('A generic warning',))
        self.assertEqual(caught[1].message.args, ('A deprecation warning',))
        self.assertEqual(caught[0].category, UserWarning)
        self.assertEqual(caught[1].category, DeprecationWarning)

    def test_nice_string_representation_of_caught_warnings(self):
        from warningutils import capture_warnings
        with capture_warnings() as caught:
            warnings.warn('A generic warning')
            self.assertEqual(len(caught), 1)
            warnings.warn('A deprecation warning', DeprecationWarning)
            self.assertEqual(len(caught), 2)
        self.assertIn("UserWarning", repr(caught[0]))
        self.assertIn("A deprecation warning", repr(caught[1]))
        self.assertIn("UserWarning", str(caught))


# To test the Bonus part of this exercise, comment out the following line
@unittest.expectedFailure
class MoreCaptureWarningsTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        warnings.resetwarnings()

    @classmethod
    def tearDownClass(cls):
        warnings.resetwarnings()

    def test_warnings_by_message_and_category(self):
        from warningutils import capture_warnings

        # Capture by message
        with redirect_stderr(StringIO()) as output:
            with capture_warnings('generic') as caught:
                warnings.warn('First generic warning')
                self.assertEqual(len(caught), 0)
            with capture_warnings('.*generic') as caught:
                warnings.warn('A generic warning')
                self.assertEqual(len(caught), 1)
                warnings.warn('A deprecation warning', DeprecationWarning)
                self.assertEqual(len(caught), 1)
            self.assertEqual(caught[0].message.args, ('A generic warning',))
            self.assertEqual(caught[0].category, UserWarning)
            self.assertIn('First generic warning', output.getvalue())
            self.assertNotIn('A generic warning', output.getvalue())
            self.assertIn('A deprecation warning', output.getvalue())

        # Capture by category
        with redirect_stderr(StringIO()) as output:
            with capture_warnings(category=UserWarning) as caught:
                warnings.warn('A generic warning')
                self.assertEqual(len(caught), 1)
            self.assertEqual(caught[0].message.args, ('A generic warning',))
            self.assertEqual(caught[0].category, UserWarning)
            self.assertNotIn('A generic warning', output.getvalue())
            with capture_warnings(category=DeprecationWarning) as caught:
                warnings.warn('Another generic warning')
                self.assertEqual(len(caught), 0)
                warnings.warn('deprecation warning', DeprecationWarning)
                self.assertEqual(len(caught), 1)
            self.assertEqual(caught[0].message.args, ('deprecation warning',))
            self.assertEqual(caught[0].category, DeprecationWarning)
            self.assertIn('Another generic warning', output.getvalue())
            self.assertNotIn('A deprecation warning', output.getvalue())

        # Nested capturing
        with redirect_stderr(StringIO()) as output:
            with capture_warnings(category=DeprecationWarning) as deprecations:
                with capture_warnings(category=UserWarning) as user_warnings:
                    with capture_warnings('.*fluffy') as fluffy_warnings:
                        warnings.warn("This is a generic warning")
                        warnings.warn("This is a fluffy warning")
                        warnings.warn("Also fluffy", DeprecationWarning)
                        warnings.warn("Another warning", DeprecationWarning)
        self.assertEqual(len(fluffy_warnings), 2)
        self.assertEqual(len(user_warnings), 1)
        self.assertEqual(len(deprecations), 1)
        self.assertEqual(output.getvalue(), "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
