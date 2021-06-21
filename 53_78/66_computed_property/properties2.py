class computed_property:
    """Decorator and descriptor.
    Inputs: Set of attributes the property depends on. Property will be recomputed (by calling the function it wraps)
    when one or more of these attributes change."""

    MISSING = object()

    def __init__(self, *attr_names):
        self.attr_names = attr_names
        self._setter = None

    def __call__(self, func):
        self._getter = func
        return self

    def setter(self, func):
        self._setter = func
        return self

    def __get__(self, instance, owner=None):
        if instance is None:  # If no instance off owner class can't compute property and have no cache
            return self

        # Check if any of our watched attributes have changed. If so, compute and update
        attr_values = tuple(getattr(instance, attr, self.MISSING) for attr in self.attr_names)
        if attr_values != getattr(instance, self.dependency_names, ()):
            setattr(instance, self.dependency_names, attr_values)
            setattr(instance, self.cached_name, self._getter(instance))

        # Make sure we have a valid return value
        if getattr(instance, self.cached_name) is self.MISSING:
            raise AttributeError(f'{type(self).__name__} cannot compute or retrieve {self.name}')

        return getattr(instance, self.cached_name)

    def __set__(self, instance, value=None):
        if self._setter is None:
            raise AttributeError(f'{type(self).__name__} cannot be set')
        else:
            self._setter(instance, value)

    def __delete__(self, instance):
        raise AttributeError(f'{type(self).__name__} cannot be deleted')

    def __set_name__(self, owner, name):
        self.dependency_names = f'{name}_dependencies'
        self.cached_name = f'{name}_value'
        self.name = name
