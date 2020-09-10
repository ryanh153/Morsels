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
