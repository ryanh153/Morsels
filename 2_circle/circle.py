import math


class Circle:
    """A class for circle objects. All have a radius, diameter and area"""

    def __init__(self, radius=1):
        if radius < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = radius
        self._diameter = 2.*radius
        self._area = math.pi*radius**2.

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        if radius < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = radius
        self._diameter = 2.*radius
        self._area = math.pi*radius**2.

    @property
    def diameter(self):
        return self._diameter

    @diameter.setter
    def diameter(self, diameter):
        if diameter < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = diameter / 2.
        self._diameter = diameter
        self._area = math.pi*self._radius**2.

    @property
    def area(self):
        return self._area

    def __repr__(self):
        return "Circle(%d)" % self._radius
