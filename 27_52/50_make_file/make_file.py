import os
import tempfile
from contextlib import contextmanager


@contextmanager
def make_file(*, contents=None, mode='wt', encoding=None, newline=None, directory=None):
    file = tempfile.NamedTemporaryFile(mode=mode, encoding=encoding, newline=newline, dir=directory, delete=False)
    if contents:
        with file:
            file.write(contents)
    try:
        yield file.name
    finally:
        os.remove(file.name)


# Original
# def _select_mode(contents):
#     if contents is None:
#         mode = 'wt'
#     else:  # infer from contents
#         if isinstance(contents, str):
#             mode = 'wt'
#         elif isinstance(contents, bytes):
#             mode = 'wb'
#         else:
#             raise ValueError(f"Contents must be string or bytes. Given {type(contents)}")
#     return mode
#
#
# class make_file:
#     def __init__(self, *, mode=None, encoding=None, newline=None, contents=None, directory=None):
#         if mode is None:
#             mode = _select_mode(contents)
#         self.file = tempfile.NamedTemporaryFile(mode=mode, encoding=encoding, newline=newline, dir=directory,
#                                                 delete=False)
#         if contents:
#             open(self.file.name, mode=mode, encoding=encoding, newline=newline).write(contents)
#
#     def __enter__(self):
#         return self.file.name
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         os.remove(self.file.name)
