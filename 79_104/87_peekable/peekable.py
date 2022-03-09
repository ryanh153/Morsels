from __future__ import annotations
from itertools import tee, chain
from typing import Iterable, Any, Union

DEFAULT = object()


class Peek:
    """A lazy iterable with the ability to peek at the next item without consuming it"""

    def __init__(self: Peek, iterable: Iterable) -> None:
        self.iterable, self.peeker = tee(iterable, 2)
        self.peeked, self.peek_val = False, None

    def peek(self: Peek, default: Any = DEFAULT) -> Any:
        if not self.peeked:
            try:
                self.peek_val = next(self.peeker)
                self.peeked = True
            except StopIteration:
                if default is not DEFAULT:
                    return default
                raise
        return self.peek_val

    def __iter__(self: Peek) -> Peek:
        return self

    def __next__(self: Peek) -> Any:
        if not self.peeked:
            next(self.peeker)
        self.peeked = False
        return next(self.iterable)

    def __bool__(self: Peek) -> bool:
        if self.peeked:
            return True
        try:
            self.peek()
            return True
        except StopIteration:
            return False

    def prepend(self: Peek, item: Any) -> None:
        self.peeked, self.peek_val = False, None  # Basically re-set the front
        prepended = chain([item], self.iterable)
        self.iterable, self.peeker = tee(prepended, 2)

    def _prepend_iterable(self: Peek, items: Iterable) -> None:
        self.peeked, self.peek_val = False, None  # re-set the front
        prepended = chain(items, self.iterable)
        self.iterable, self.peeker = tee(prepended)

    def __getitem__(self: Peek, index: Union[int, slice]) -> Any:
        if isinstance(index, slice):
            vals = list()
            for _ in range(index.stop):
                try:
                    vals.append(next(self))
                except StopIteration:
                    break
            self._prepend_iterable(vals)
            return vals
        vals = [next(self) for _ in range(index + 1)]
        self._prepend_iterable(vals)
        return vals[-1]


def peekable(iterable: Iterable) -> Peek:
    return Peek(iterable)
