not_cached = object()


class computed_property:

    def __init__(self, attr_name):
        self.attr_name = attr_name
        self.cached_attr, self.cached_value = not_cached, not_cached

    def __call__(self, func):
        self.func = func
        return self

    def __get__(self, instance, owner=None):
        if getattr(instance, self.attr_name) != self.cached_attr:
            self.cached_attr = getattr(instance, self.attr_name)
            self.cached_value = self.func(instance)
        return self.cached_value

    def __set__(self, instance, value=None):
        raise AttributeError(f'{type(self).__name__} cannot be set')

    def __delete__(self, instance):
        raise AttributeError(f'{type(self).__name__} cannot be deleted')
#
#
# class Circle:
#     def __init__(self, radius=1):
#         self.radius = radius
#
#     @computed_property('radius')
#     def diameter(self):
#         print('computing diameter')
#         print(self)
#         return self.radius * 2
#
#
# # print('making c')
# c = Circle()
# # print('about to call')
# # print(c.diameter)
# # print(c.diameter)
# c.diameter = 3
