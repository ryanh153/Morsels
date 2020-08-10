import os
from contextlib import nullcontext
from tempfile import TemporaryDirectory


class cd:
    def __init__(self, directory=None):
        self.tmpdir = nullcontext(directory) if directory else TemporaryDirectory()

    def __enter__(self):
        self.current = self.tmpdir.__enter__()  # returns the context manager to the appropriate path
        self.previous = os.getcwd()
        os.chdir(self.current)
        return self

    def enter(self):
        self.__enter__()

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        os.chdir(self.previous)
        self.tmpdir.__exit__(exc_type, exc_val, exc_tb)  # exit so we delete the temp directory if we created one

    def exit(self, ):
        self.__exit__()
