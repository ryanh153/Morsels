from contextlib import contextmanager, redirect_stderr, redirect_stdout
from io import StringIO
from importlib.machinery import SourceFileLoader
import os
import sys
from textwrap import dedent
from tempfile import NamedTemporaryFile
import unittest
import warnings


class SortByColumnTests(unittest.TestCase):

    """Tests for sort_by_column.py"""

    maxDiff = None

    def test_sort_by_first_column(self):
        contents = dedent("""
            2012,Lexus,LFA
            2009,GMC,Yukon XL 1500
            1965,Ford,Mustang
            2005,Hyundai,Sonata
            1995,Mercedes-Benz,C-Class
        """).lstrip()
        expected = dedent("""
            1965,Ford,Mustang
            1995,Mercedes-Benz,C-Class
            2005,Hyundai,Sonata
            2009,GMC,Yukon XL 1500
            2012,Lexus,LFA
        """).lstrip().replace('\n', '\r\n')
        with make_file(contents) as csv_file:
            output = run_program('sort_by_column.py', args=[csv_file, '0'])
        self.assertEqual(expected.splitlines(), output.splitlines())

    def test_sort_by_second_column(self):
        contents = dedent("""
            2012,Lexus,LFA
            2009,GMC,Yukon XL 1500
            1965,Ford,Mustang
            2005,Hyundai,Sonata
            1995,Mercedes-Benz,C-Class
        """).lstrip()
        expected = dedent("""
            1965,Ford,Mustang
            2009,GMC,Yukon XL 1500
            2005,Hyundai,Sonata
            2012,Lexus,LFA
            1995,Mercedes-Benz,C-Class
        """).lstrip().replace('\n', '\r\n')
        with make_file(contents) as csv_file:
            output = run_program('sort_by_column.py', args=[csv_file, '1'])
        self.assertEqual(expected.splitlines(), output.splitlines())

    def test_original_file_is_unchanged(self):
        old_contents = dedent("""
            2012,Lexus,LFA
            2009,GMC,Yukon XL 1500
        """).lstrip()
        with make_file(old_contents) as filename:
            run_program('sort_by_column.py', args=[filename, '0'])
            with open(filename) as csv_file:
                new_contents = csv_file.read()
        self.assertEqual(old_contents.splitlines(), new_contents.splitlines())

    def test_sorting_with_commas(self):
        contents = dedent("""
            "Hughes, John",Baby's Day Out
            "Hughes, John",The Breakfast Club
            "Hughes, Langston",A Dream Deferred
            "Hughes, Langston",Dreams
        """).lstrip().replace('\n', '\r\n')
        expected = dedent("""
            "Hughes, Langston",A Dream Deferred
            "Hughes, John",Baby's Day Out
            "Hughes, Langston",Dreams
            "Hughes, John",The Breakfast Club
        """).lstrip().replace('\n', '\r\n')
        with make_file(contents) as old:
            output = run_program('sort_by_column.py', args=[old, '1'])
        self.assertEqual(expected.splitlines(), output.splitlines())

    def test_sort_by_one_column_only(self):
        contents = dedent("""
            11,Johnny Cash,Folsom Prison Blues
            13,Billy Joe Shaver,Low Down Freedom
            2,Waylon Jennings,Honky Tonk Heroes (Like Me)
            2,Hank Williams III,Mississippi Mud
            4,Kris Kristofferson,To Beat The Devil
            22,David Allan Coe,"Willie, Waylon, And Me"
            4,Bob Dylan,House Of The Risin' Sun
        """).lstrip().replace('\n', '\r\n')
        expected = dedent("""
            11,Johnny Cash,Folsom Prison Blues
            13,Billy Joe Shaver,Low Down Freedom
            2,Waylon Jennings,Honky Tonk Heroes (Like Me)
            2,Hank Williams III,Mississippi Mud
            22,David Allan Coe,"Willie, Waylon, And Me"
            4,Kris Kristofferson,To Beat The Devil
            4,Bob Dylan,House Of The Risin' Sun
        """).lstrip().replace('\n', '\r\n')
        with make_file(contents) as old:
            output = run_program('sort_by_column.py', args=[old, '0'])
        self.assertEqual(expected.splitlines(), output.splitlines())

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_sort_by_multiple_columns(self):
        contents = dedent("""
            2005,Lexus,LFA
            2009,GMC,Yukon XL 1500
            1995,Ford,Mustang
            2005,Hyundai,Sonata
            1995,Mercedes-Benz,C-Class
        """).lstrip()
        expected = dedent("""
            1995,Mercedes-Benz,C-Class
            1995,Ford,Mustang
            2005,Lexus,LFA
            2005,Hyundai,Sonata
            2009,GMC,Yukon XL 1500
        """).lstrip().replace('\n', '\r\n')
        with make_file(contents) as name:
            output = run_program('sort_by_column.py', args=[name, '0', '2'])
        self.assertEqual(expected.splitlines(), output.splitlines())

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_with_header(self):
        contents = dedent("""
            Track,Artist,Title
            11,Johnny Cash,Folsom Prison Blues
            13,Billy Joe Shaver,Low Down Freedom
            2,Hank Williams III,Mississippi Mud
            2,Waylon Jennings,Honky Tonk Heroes (Like Me)
            4,Kris Kristofferson,To Beat The Devil
            22,David Allan Coe,"Willie, Waylon, And Me"
            4,Bob Dylan,House Of The Risin' Sun
        """).lstrip().replace('\n', '\r\n')
        expected = dedent("""
            Track,Artist,Title
            11,Johnny Cash,Folsom Prison Blues
            13,Billy Joe Shaver,Low Down Freedom
            2,Hank Williams III,Mississippi Mud
            2,Waylon Jennings,Honky Tonk Heroes (Like Me)
            22,David Allan Coe,"Willie, Waylon, And Me"
            4,Kris Kristofferson,To Beat The Devil
            4,Bob Dylan,House Of The Risin' Sun
        """).lstrip().replace('\n', '\r\n')
        with make_file(contents) as old:
            output = run_program('sort_by_column.py',
                                 args=[old, '--with-header', '0'])
        self.assertEqual(expected.splitlines(), output.splitlines())

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_sort_with_column_type(self):
        contents = dedent("""
            11,Johnny Cash,Folsom Prison Blues
            13,Billy Joe Shaver,Low Down Freedom
            2,Waylon Jennings,Honky Tonk Heroes (Like Me)
            2,Hank Williams III,Mississippi Mud
            4,Kris Kristofferson,To Beat The Devil
            22,David Allan Coe,"Willie, Waylon, And Me"
            4,Bob Dylan,House Of The Risin' Sun
        """).lstrip().replace('\n', '\r\n')
        expected = dedent("""
            2,Hank Williams III,Mississippi Mud
            2,Waylon Jennings,Honky Tonk Heroes (Like Me)
            4,Bob Dylan,House Of The Risin' Sun
            4,Kris Kristofferson,To Beat The Devil
            11,Johnny Cash,Folsom Prison Blues
            13,Billy Joe Shaver,Low Down Freedom
            22,David Allan Coe,"Willie, Waylon, And Me"
        """).lstrip().replace('\n', '\r\n')
        with make_file(contents) as old:
            output = run_program('sort_by_column.py', args=[old, '0:num', '1:str'])
        self.assertEqual(expected.splitlines(), output.splitlines())


class DummyException(Exception):
    """No code will ever raise this exception."""


def run_program(path, args=[], raises=DummyException):
    """
    Run program at given path with given arguments.

    If raises is specified, ensure the given exception is raised.
    """
    old_args = sys.argv
    warnings.simplefilter("ignore", ResourceWarning)
    assert all(isinstance(a, str) for a in args)
    try:
        sys.argv = [path] + args
        with redirect_stderr(StringIO()) as output:
            with redirect_stdout(output):
                try:
                    if '__main__' in sys.modules:
                        del sys.modules['__main__']
                    SourceFileLoader('__main__', path).load_module()
                except raises:
                    return output.getvalue()
                except SystemExit as e:
                    if e.args != (0,):
                        raise SystemExit(output.getvalue()) from e
                if raises is not DummyException:
                    raise AssertionError("{} not raised".format(raises))
                return output.getvalue()
    finally:
        sys.argv = old_args


@contextmanager
def make_file(contents=None):
    """Context manager providing name of a file containing given contents."""
    with NamedTemporaryFile(
            mode='wt',
            encoding='utf-8',
            newline='',
            delete=False,
    ) as f:
        if contents:
            f.write(contents)
    try:
        yield f.name
    finally:
        os.remove(f.name)


if __name__ == "__main__":
    unittest.main(verbosity=2)