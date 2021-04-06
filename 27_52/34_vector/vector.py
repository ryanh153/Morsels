from dataclasses import astuple, dataclass
from numbers import Number


@dataclass(frozen=True)
class Vector:

    x: Number
    y: Number
    z: Number

    __slots__ = ('x', 'y', 'z')

    def __iter__(self):
        yield from astuple(self)

    def __eq__(self, other):
        if isinstance(other, Vector):
            return tuple(self) == tuple(other)
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(* (a + b for a, b in zip(self, other)))
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(*(a - b for a, b in zip(self, other)))
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Number):
            return Vector(*(a * other for a in self))
        return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, Number):
            return Vector(*(a / other for a in self))
        return NotImplemented
