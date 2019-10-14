# Thoughts: diameter and area are calculated each time they are asked for. Store them (_diameter, etc)?
# it would require more lines in the setters because you'd have to change all 3 internals every time either
# radius or diameter is set.
import math

# diameter/area are calculate every time they're asked for.
# more expensive gets, less expensive sets
# class Circle:
#     """A class for circle objects. All have a radius, diameter and area"""
#
#     def __init__(self, radius=1):
#         if radius < 0:
#             raise ValueError("Radius cannot be negative")
#         self._radius = radius
#
#     @property
#     def radius(self):
#         return self._radius
#
#     @radius.setter
#     def radius(self, radius):
#         if radius < 0:
#             raise ValueError("Radius cannot be negative")
#         self._radius = radius
#
#     @property
#     def diameter(self):
#         return 2. * self._radius
#
#     @diameter.setter
#     def diameter(self, diameter):
#         self._radius = diameter / 2.
#
#     @property
#     def area(self):
#         return math.pi * self._radius ** 2.
#
#     def __repr__(self):
#         return "Circle(%d)" % self._radius


# when r/d are changed internals for all 3 are updated.
# More expensive sets, less expensive gets
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
        self._radius = diameter / 2.
        self._diameter = diameter
        self._area = math.pi*self._radius**2.

    @property
    def area(self):
        return self._area

    def __repr__(self):
        return "Circle(%d)" % self._radius
