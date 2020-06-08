class alias:

    def __init__(self, attr, *, write=False):
        self.attr = attr
        self.write = write

    def __get__(self, obj, object_type):
        if obj is None:
            return getattr(object_type, self.attr)
        else:
            return getattr(obj, self.attr)

    def __set__(self, obj, value):
        if self.write:
            return setattr(obj, self.attr, value)
        else:
            raise AttributeError("Can't set alias.")
