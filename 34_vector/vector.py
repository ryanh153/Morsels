class Vector:

    __slots__ = ('x', 'y', 'z')

    def __init__(self, x, y, z):
        super(Vector, self).__setattr__('x', x)
        super(Vector, self).__setattr__('y', y)
        super(Vector, self).__setattr__('z', z)

    def __iter__(self):
        yield from (self.x, self.y, self.z)

    def __eq__(self, other):
        if isinstance(other, Vector):
            if (self.x, self.y, self.z) == (other.x, other.y, other.z):
                return True
        return False

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            return NotImplemented

    def __mul__(self, other):
        try:
            other = float(other)
            return Vector(self.x * other, self.y * other, self.z * other)
        except ValueError:
            return NotImplemented

    def __rmul__(self, other):
        try:
            other = float(other)
            return Vector(self.x * other, self.y * other, self.z * other)
        except ValueError:
            return NotImplemented

    def __truediv__(self, other):
        try:
            other = float(other)
            return Vector(self.x / other, self.y / other, self.z / other)
        except ValueError:
            return NotImplemented

    def __setattr__(self, key, value):
        raise AttributeError("Vectors are immutable")
