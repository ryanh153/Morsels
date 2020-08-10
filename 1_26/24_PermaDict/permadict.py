class PermaDict(dict):

    def __init__(self, *args, **kwargs):
        self.silent = False
        if "silent" in kwargs.keys():
            self.silent = True
            kwargs.__delitem__("silent")

        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if key in self.keys():
            if self.silent:
                pass
            else:
                raise KeyError
        else:
            super().__setitem__(key, value)

    def update(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError("update expected at most 1 arguments, got 2")

        if len(kwargs) and "force" in kwargs.keys():  # if we're forcing just use normal dict() update
            kwargs.__delitem__("force")
            super().update(*args, **kwargs)
        else:
            new_dict = {}
            if len(args):  # got a positional. Must be either a dict or a list of (key, value) pairs
                if isinstance(args[0], dict):
                    new_dict = args[0]
                else:
                    new_dict = dict(args[0])
            elif len(kwargs):  # or we got a set of keyword arguments that are key/value pairs. Make dict from
                new_dict = kwargs

            for key, value in new_dict.items():
                self.__setitem__(key, value)

    def force_set(self, key, value):
        super().__setitem__(key, value)
