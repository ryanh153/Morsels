from io import StringIO
from contextlib import contextmanager, redirect_stdout, redirect_stderr
import builtins
from os import linesep


class WriteSpy:

    def __init__(self, *files, close=True):
        self.files = [file for file in files]
        self._close = close
        self.closed = False

    def __enter__(self):
        self._open_all_files()
        self.closed = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            raise exc_type(exc_val, exc_tb)
        if self._close:
            self._close_all_files()
        self.closed = True

    def write(self, string):
        if self.closed:
            raise IOError(f'Writing to closed {self!r}')
        for file in self.files:
            file.write(string)

    def close(self):
        if self._close:
            self._close_all_files()
        self.closed = True

    def writable(self):
        if self.closed:
            return False
        return all([file.writable() for file in self.files])

    def _close_all_files(self):
        for file in self.files:
            if hasattr(file, 'close'):
                file.close()

    def _open_all_files(self):
        for file in self.files:
            if hasattr(file, 'open'):
                file.open()


class Spy:

    def __init__(self):
        self.stored = StringIO()

    def write(self, string):
        self.stored.write(string)


@contextmanager
def stdout_spy():
    spy = Spy()
    with redirect_stdout(spy):
        yield spy.stored
    print(spy.stored.getvalue()[:-1])  # Strip last newline character


@contextmanager
def stdin_spy():
    def my_input(*args, **kwargs):
        # Call the normal input but store the result
        response = original_input(*args, **kwargs)
        stored.write(response + '\n')
        return response

    stored = StringIO()
    original_input = getattr(builtins, 'input')
    setattr(builtins, 'input', my_input)
    try:
        yield stored
    finally:
        setattr(builtins, 'input', original_input)


class StringSpy:

    def __init__(self):
        self.stored = ''

    def write(self, string):
        self.stored += string


class BetterSpy:

    def __init__(self):
        self.stdin = ''
        self._stdout = StringSpy()
        self._stderr = StringSpy()

    @property
    def stdout(self):
        return self._stdout.stored

    @property
    def stderr(self):
        return self._stderr.stored


@contextmanager
def iospy():
    def my_input(*args, **kwargs):
        # Call the normal input but store the result
        response = original_input(*args, **kwargs)
        context_spy.stdin += f'{response}{linesep}'
        return response

    context_spy = BetterSpy()
    original_input = getattr(builtins, 'input')
    setattr(builtins, 'input', my_input)
    with redirect_stdout(context_spy._stdout), redirect_stderr(context_spy._stderr):
        yield context_spy

    print(context_spy.stdout.strip('\n'), end='')  # Drop last newline and don't add any
    setattr(builtins, 'input', original_input)
