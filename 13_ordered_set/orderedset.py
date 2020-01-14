class OrderedSet:

    def __init__(self, set_items):
        """Takes an iterable of items and adds them in order to an container
        that maintains order, but does not allow repeated entries."""

        self.n = 0  # for iterating over set
        self.set = set()
        self.ordered_set = []
        for item in set_items:
            if item not in self.set:
                self.set.add(item)
                self.ordered_set.append(item)

    def add(self, other):
        if other not in self.set:
            self.set.add(other)
            self.ordered_set.append(other)

    def discard(self, other):
        if other in self.set:
            self.set.discard(other)
            self.ordered_set.remove(other)

    def __eq__(self, other):
        if isinstance(other, OrderedSet) or isinstance(other, set):  # check for different sizes
            if len(other) != len(self):
                return False

        if isinstance(other, OrderedSet):  # check for items and order if OrderedSet
            for obj1, obj2 in zip(self.ordered_set, other.ordered_set):
                if obj1 != obj2:
                    break
            else:
                return True
            return False

        elif isinstance(other, set):  # check only for item containment is set
            for obj in self.ordered_set:
                if obj not in other:
                    break
            else:
                return True
            return False

        else:  # if not set or OrderedSet return False
            return False

    def __contains__(self, other):
        if other in self.set:
            return True

    def __next__(self):
        if self.n < len(self.ordered_set):
            result = self.ordered_set[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    def __len__(self):
        return len(self.ordered_set)

    def __iter__(self):
        return iter(self.ordered_set)

    def __getitem__(self, item):
        return self.ordered_set[item]
