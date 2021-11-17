import sys
from io import TextIOBase, StringIO
from contextlib import contextmanager, redirect_stdout, redirect_stderr


class WriteSpy(TextIOBase):

    def __init__(self, stream, spy, close=True):
        self.stream = stream
        self.spy = spy
        self._close = close

    def write(self, text):
        self._checkClosed()
        self.stream.write(text)
        self.spy.write(text)

    def writable(self) -> bool:
        self._checkClosed()
        return True

    def close(self):
        if self._close:
            self.stream.close()
            self.spy.close()
        super().close()


@contextmanager
def stdout_spy():
    logged = StringIO()
    with redirect_stdout(WriteSpy(sys.stdout, logged, close=False)):
        yield logged


class ReadSpy(TextIOBase):

    def __init__(self, stream, spy):
        self.stream = stream
        self.spy = spy

    def read(self):
        result = self.stream.read()
        self.spy.write(result)
        return result

    def readline(self):
        result = self.stream.readline()
        self.spy.write(result)
        return result


@contextmanager
def stdin_spy():
    logged = StringIO()
    real_stdin, sys.stdin = sys.stdin, ReadSpy(sys.stdin, logged)
    yield logged
    sys.stdin = real_stdin


class Spy:

    def __init__(self, out_spy, in_spy, err_spy):
        self.out_spy = out_spy
        self.in_spy = in_spy
        self.err_spy = err_spy

    @property
    def stdout(self):
        return self.out_spy.spy.getvalue()

    @property
    def stdin(self):
        return self.in_spy.spy.getvalue()

    @property
    def stderr(self):
        return self.err_spy.spy.getvalue()


@contextmanager
def iospy():
    out_logged, in_logged, err_logged = StringIO(), StringIO(), StringIO()
    out_spy = WriteSpy(sys.stdout, out_logged, close=False)
    in_spy = ReadSpy(sys.stdin, in_logged)
    err_spy = WriteSpy(sys.stderr, err_logged, close=False)

    real_stdin, sys.stdin = sys.stdin, in_spy
    spy = Spy(out_spy, in_spy, err_spy)

    with redirect_stdout(out_spy), redirect_stderr(err_spy):
        yield spy
    sys.stdin = real_stdin
