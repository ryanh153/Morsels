class Point:
    """A 3D point object, defined by x,y,z coordinates"""

    def __init__(self, x, y, z):
        """Initialize a point object from x,y, and z coordinates"""
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        """Define string representation of Points."""
        return f"Point(x={self.x}, y={self.y}, z={self.z})"

    def __eq__(self, other):
        """Two Points are equal iff their x,y and z coordinates are the same."""
        result = True
        if not isinstance(other, Point):
            result = False
        elif self.x != other.x:
            result = False
        elif self.y != other.y:
            result = False
        elif self.z != other.z:
            result = False
        return result
    
    def __sub__(self, other):
        """Subtract x,y, and z coordiante of two Points (new_x = x1-x2 etc)."""
        if not isinstance(other, Point):
            raise ValueError("Tried to subtract a Point and a non-Point")
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        """Add x,y, and z coordiante of two Points (new_x = x1+x2 etc)."""
        if not isinstance(other, Point):
            raise ValueError("Tried to add a Point and a non-Point")
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other):
        """Multiply each coordiante of a Point by a scalar"""
        return Point(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        """Multiplication if Point is on the right side of the operation."""
        return self*other

    def __iter__(self):
        """Allow unpacking of points (i.e. p1 = Point(1,2,3); x, y, z = p1)"""
        return iter((self.x, self.y, self.z))
