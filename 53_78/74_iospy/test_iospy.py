from contextlib import contextmanager, redirect_stdout
from io import StringIO
import sys
import unittest

from iospy import WriteSpy


class WriteSpyTests(unittest.TestCase):

    """Tests for WriteSpy"""

    def test_writing_to_two_files(self):
        f1, f2 = StringIO(), StringIO()
        combined = WriteSpy(f1, f2)
        print('Hello world!', file=combined)
        self.assertEqual(f1.getvalue(), 'Hello world!\n')
        self.assertEqual(f2.getvalue(), 'Hello world!\n')
        combined.write('More things!\n')
        self.assertEqual(f1.getvalue(), 'Hello world!\nMore things!\n')
        self.assertEqual(f2.getvalue(), 'Hello world!\nMore things!\n')

    def test_writable(self):
        f1, f2 = StringIO(), StringIO()
        combined = WriteSpy(f1, f2)
        self.assertTrue(combined.writable())

    def test_close(self):
        f1, f2 = StringIO(), StringIO()
        combined = WriteSpy(f1, f2)
        combined.close()
        with self.assertRaises(Exception):
            combined.write('hello')
        with self.assertRaises(Exception):
            self.assertTrue(combined.writable())
        combined.close()
        with self.assertRaises(Exception):
            f1.getvalue()
        with self.assertRaises(Exception):
            f2.getvalue()

    def test_no_close(self):
        f1, f2 = StringIO(), StringIO()
        combined = WriteSpy(f1, f2, close=False)
        combined.write('hi')
        combined.close()
        self.assertEqual(f1.getvalue(), 'hi')
        self.assertEqual(f2.getvalue(), 'hi')
        with self.assertRaises(Exception):
            combined.write('hello')
        with self.assertRaises(Exception):
            self.assertTrue(combined.writable())
        combined.close()
        self.assertTrue(combined.closed)
        self.assertEqual(f1.getvalue(), 'hi')
        self.assertEqual(f2.getvalue(), 'hi')

    def test_context_manager(self):
        f1, f2 = StringIO(), StringIO()
        with WriteSpy(f1, f2, close=False) as combined:
            combined.write('hello')
            self.assertFalse(combined.closed)
        self.assertEqual(f1.getvalue(), 'hello')
        self.assertEqual(f2.getvalue(), 'hello')
        with WriteSpy(f1, f2) as combined:
            combined.write('hello')
            self.assertFalse(combined.closed)
            self.assertEqual(f1.getvalue(), 'hellohello')
        self.assertTrue(combined.closed)
        self.assertTrue(f1.closed)
        with self.assertRaises(Exception):
            combined.write('hello')


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class StdoutSpyTests(unittest.TestCase):

    """Tests for stdout_spy"""

    def test_no_output(self):
        from iospy import stdout_spy
        with stdout_spy() as spied_stdout:
            self.assertEqual(spied_stdout.getvalue(), '')
        self.assertEqual(spied_stdout.getvalue(), '')

    def test_original_output_maintained(self):
        from iospy import stdout_spy
        with redirect_stdout(StringIO()) as mock_stdout:
            with stdout_spy():
                print('First line')
                print('Second line')
        self.assertEqual(mock_stdout.getvalue(), 'First line\nSecond line\n')

    def test_output_captured(self):
        from iospy import stdout_spy
        with redirect_stdout(StringIO()):
            with stdout_spy() as spied_stdout:
                print('First line')
                print('Second line')
        self.assertEqual(spied_stdout.getvalue(), 'First line\nSecond line\n')


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class StdinSpyTests(unittest.TestCase):

    """Tests for stdin_spy"""

    def test_no_input(self):
        from iospy import stdin_spy
        with stdin_spy() as spied_stdin:
            self.assertEqual(spied_stdin.getvalue(), '')

    def test_user_prompted(self):
        from iospy import stdin_spy
        with redirect_stdout(StringIO()) as stdout:
            with patch_stdin("Trey\npurple\n"):
                with stdin_spy() as spied_stdin:
                    # print(input)
                    name = input("What's your name? ")
                    color = input("What's your favorite color? ")
        # self.assertEqual(spied_stdin.getvalue(), "Trey\npurple\n")
        self.assertEqual(name, "Trey")
        self.assertEqual(color, "purple")
        self.assertEqual(
            stdout.getvalue(),
            "What's your name? What's your favorite color? ",
        )


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class IOSpyTests(unittest.TestCase):

    """Tests for iospy"""

    def test(self):
        from iospy import iospy
        with redirect_stdout(StringIO()) as stdout:
            with patch_stdin("Trey\npurple\n"):
                with iospy() as spied:
                    name = input("What's your name? ")
                    color = input("What's your favorite color? ")
                    if color != "black":
                        print("{} isn't black".format(color), file=sys.stderr)
        self.assertEqual(spied.stderr, "purple isn't black\n")
        self.assertEqual(
            spied.stdout,
            "What's your name? What's your favorite color? ",
        )
        self.assertEqual(spied.stdin, "Trey\npurple\n")
        self.assertEqual(name, "Trey")
        self.assertEqual(color, "purple")
        self.assertEqual(
            stdout.getvalue(),
            "What's your name? What's your favorite color? ",
        )


@contextmanager
def patch_stdin(text):
    real_stdin = sys.stdin
    sys.stdin = StringIO(text)
    try:
        yield sys.stdin
    except EOFError as e:
        raise AssertionError("Read more input than was given") from e
    finally:
        sys.stdin = real_stdin


if __name__ == "__main__":
    unittest.main(verbosity=2)