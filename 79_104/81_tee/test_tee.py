from contextlib import contextmanager, redirect_stdout, redirect_stderr
from io import BytesIO, TextIOWrapper
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import os
from pathlib import Path
import sys
from tempfile import NamedTemporaryFile
import unittest
import warnings


class TeeTests(unittest.TestCase):

    """Tests for tee.py"""

    def test_no_input(self):
        with patch_stdin(""):
            output = run_program('tee.py')
            self.assertEqual(output, "")

    def test_one_line(self):
        with patch_stdin("hello\n"):
            output = run_program('tee.py')
            self.assertEqual(output, "hello\n")

    def test_four_lines(self):
        text = "Line 1\nLine 2\nLine 3\n"
        with patch_stdin(text):
            output = run_program('tee.py')
            self.assertEqual(output, text)

    def test_no_line_ending(self):
        with patch_stdin("hello"):
            output = run_program('tee.py')
            self.assertEqual(output, "hello")

    def test_pipe_to_one_file(self):
        text = "This is a file\nWith multiple lines in it\n\nThe end."
        with make_file() as filename:
            with patch_stdin(text):
                output = run_program('tee.py', [filename])
            self.assertEqual(output, text)
            self.assertEqual(Path(filename).read_text(), text)

    def test_pipe_to_file_twice(self):
        text1 = "This is a file\n"
        text2 = "This is the second write\n"
        with make_file() as filename:
            with patch_stdin(text1):
                output1 = run_program('tee.py', [filename])
            self.assertEqual(output1, text1)
            self.assertEqual(Path(filename).read_text(), text1)
            with patch_stdin(text2):
                output2 = run_program('tee.py', [filename])
            self.assertEqual(output2, text2)
            self.assertEqual(Path(filename).read_text(), text2)

    def test_pipe_to_nonexistant_file(self):
        text = "This is a file\nWith multiple lines in it\n\nThe end."
        with make_file() as filename:
            Path(filename).unlink()
            with patch_stdin(text):
                output = run_program('tee.py', [filename])
            self.assertEqual(output, text)
            self.assertEqual(Path(filename).read_text(), text)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_pipe_to_many_files(self):
        text = "This is a file\nWith multiple lines in it\n\nThe end."
        with make_file() as file1, make_file() as file2, make_file() as file3:
            with patch_stdin(text):
                output = run_program('tee.py', [file1, file2, file3])
            self.assertEqual(output, text)
            self.assertEqual(Path(file1).read_text(), text)
            self.assertEqual(Path(file2).read_text(), text)
            self.assertEqual(Path(file3).read_text(), text)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_binary_input_and_output(self):
        binary_data = bytes(range(256))
        with make_file() as filename:
            with patch_stdin(binary_data):
                output = run_program('tee.py', [filename], raw_output=True)
            # self.assertEqual(output, binary_data)
            self.assertEqual(Path(filename).read_bytes(), binary_data)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_append_attribute(self):
        run1_text = "Write this to a file\nAnd this line also"
        run2_text = ".\nThis would be the third line\nAnd this the fourth"
        with make_file() as file1, make_file() as file2, make_file() as file3:
            with patch_stdin(run1_text):
                out1 = run_program('tee.py', ['-a', file1, file2, file3])
            self.assertEqual(out1, run1_text)
            self.assertEqual(Path(file1).read_text(), run1_text)
            self.assertEqual(Path(file2).read_text(), run1_text)
            self.assertEqual(Path(file3).read_text(), run1_text)
            with patch_stdin(run2_text):
                out2 = run_program('tee.py', [file1, file2, file3, '--append'])
            self.assertEqual(out2, run2_text)
            self.assertEqual(Path(file1).read_text(), run1_text + run2_text)
            self.assertEqual(Path(file2).read_text(), run1_text + run2_text)
            self.assertEqual(Path(file3).read_text(), run1_text + run2_text)


class DummyException(Exception):
    """No code will ever raise this exception."""


def run_program(path, args=[], raises=DummyException, raw_output=False):
    """
    Run program at given path with given arguments.

    If raises is specified, ensure the given exception is raised.
    """
    old_args = sys.argv
    assert all(isinstance(a, str) for a in args)
    warnings.simplefilter("ignore", ResourceWarning)
    try:
        sys.argv = [path] + args
        output = TextIOWrapper(
            PermanentBytesIO(),
            encoding=sys.stdout.encoding,
            write_through=True,
        )
        if '__main__' in sys.modules:
            del sys.modules['__main__']
        try:
            with redirect_stdout(output):
                with redirect_stderr(output):
                    loader = SourceFileLoader('__main__', path)
                    spec = spec_from_loader(loader.name, loader)
                    module = module_from_spec(spec)
                    sys.modules['__main__'] = module
                    loader.exec_module(module)
        except raises:
            pass  # Correct exceptions caught, return output
        except SystemExit as e:
            if e.args != (0,):
                raise SystemExit(output.buffer.getvalue()) from e
        else:
            if raises is not DummyException:
                raise AssertionError("{} not raised".format(raises))
        finally:
            sys.modules.pop('__main__', None)
        try:
            byte_output = output.buffer.getvalue()
            if raw_output:
                return byte_output
            else:
                return (byte_output
                        .decode(output.encoding)
                        .replace(os.linesep, "\n"))
        except ValueError as e:
            raise ValueError("Error: sys.stdout was closed") from e
    finally:
        sys.argv = old_args


@contextmanager
def make_file(contents=None, encoding=None):
    """Context manager providing name of a file containing given contents."""
    with NamedTemporaryFile(mode='wt', encoding=encoding, delete=False) as f:
        if contents:
            f.write(contents)
    try:
        yield f.name
    finally:
        os.remove(f.name)


@contextmanager
def patch_stdin(text):
    real_stdin = sys.stdin
    if isinstance(text, str):
        text = text.encode(sys.stdin.encoding)
    sys.stdin = TextIOWrapper(
        PermanentBytesIO(text),
        encoding=sys.stdin.encoding,
        write_through=True,
    )
    try:
        yield sys.stdin
    except EOFError as e:
        raise AssertionError("Read more input than was given") from e
    finally:
        sys.stdin = real_stdin


class PermanentBytesIO(BytesIO):

    _closed = False

    def close(self):
        self._closed = True

    @property
    def closed(self):
        return self._closed


if __name__ == "__main__":
    unittest.main(verbosity=2)
