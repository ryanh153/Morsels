from collections import UserString


class MutableString(UserString):

    def __setitem__(self, index, value):
        lst = [c for c in self.data]
        lst[index] = value
        self.data = "".join(lst)

    def __delitem__(self, index):
        lst = [c for c in self.data]
        del lst[index]
        self.data = "".join(lst)

    def append(self, value):
        self.data = self.data + value

    def insert(self, index, value):
        lst = [c for c in self.data]
        lst.insert(index, value)
        self.data = "".join(lst)

    def pop(self, index=-1):
        popped = self.data[index]
        lst = [c for c in self.data]
        del lst[index]
        self.data = "".join(lst)
        return MutableString(popped)
