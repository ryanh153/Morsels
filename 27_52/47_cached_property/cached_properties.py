from uuid import uuid4


class cached_property:
    def __init__(self, fget=None, fset=None, fdel=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.attr = 'property_' + uuid4().hex  # unique string that will be our attribute name

    def __get__(self, instance, owner):
        if not instance:
            return self
        elif not self.fget:
            raise AttributeError("No getter")
        elif not hasattr(instance, self.attr):
            setattr(instance, self.attr, self.fget(instance))
        return getattr(instance, self.attr)

    def __set__(self, instance, value):
        if self.fset:
            self.fset(instance, value)
        setattr(instance, self.attr, value)

    def __delete__(self, instance):
        if self.fdel:
            self.fdel(instance)
        delattr(instance, self.attr)

    def setter(self, fset):
        return cached_property(self.fget, fset=fset)

    def deleter(self, fdel):
        return cached_property(self.fget, fdel=fdel)

class Circle:
    def __init__(self, radius):
        self.radius = radius

    @cached_property
    def diameter(self):
        return self.radius * 2

    @diameter.setter
    def diameter(self, diameter):
        self.radius = diameter / 2.0

    @diameter.deleter
    def diameter(self):
        # This is a silly example
        self.radius = 0


c1 = Circle(5)
c2 = Circle(7)
print(f'D = {c1.diameter}\n')
print(f'D = {c2.diameter}\n')
c1.diameter = 20
del c1.diameter
