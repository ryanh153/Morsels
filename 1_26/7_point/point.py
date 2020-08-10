class Point:
    """A 3D point object, defined by x,y,z coordinates"""

    def __init__(self, x, y, z):
        """Initialize a point object from x,y, and z coordinates"""
        self.x, self.y, self.z = (x, y, z)

    def __repr__(self):
        """Define string representation of Points."""
        return f"Point(x={self.x}, y={self.y}, z={self.z})"

    def __eq__(self, other):
        """Two Points are equal iff their x,y and z coordinates are the same."""
        return tuple(self) == tuple(other)
    
    def __sub__(self, other):
        """Subtract x,y, and z coordiante of two Points (new_x = x1-x2 etc)."""
        return Point(*(c1-c2 for (c1, c2) in zip(self, other)))

    def __add__(self, other):
        """Add x,y, and z coordiante of two Points (new_x = x1+x2 etc)."""
        return Point(*(c1+c2 for (c1, c2) in zip(self, other)))

    def __mul__(self, other):
        """Multiply each coordiante of a Point by a scalar"""
        return Point(*(coord*other for coord in self))

    def __rmul__(self, other):
        """Multiplication if Point is on the right side of the operation."""
        return self*other

    def __iter__(self):
        """Allow unpacking of points (i.e. p1 = Point(1,2,3); x, y, z = p1)"""
        yield from (self.x, self.y, self.z)
