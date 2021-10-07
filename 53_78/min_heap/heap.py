from heapq import heapify, heappop, heappush


class Comparator:
    __slots__ = 'key', 'data', 'item'

    def __init__(self, value, key=None):
        self.key = key
        self.data = (value if key is None else key(value), value)
        self.item = value

    def __lt__(self, other):
        return self.data < other.data


class InverseComparator(Comparator):

    def __lt__(self, other):
        return other.data < self.data


class MinHeap:
    __slots__ = ('key', 'heap')
    COMPARATOR = Comparator

    def __init__(self, iterable, key=None):
        self.key = key
        self.heap = [self.COMPARATOR(val, key) for val in iterable]
        heapify(self.heap)

    def peek(self):
        return self.heap[0].item

    def pop(self):
        return heappop(self.heap).item

    def push(self, item):
        heappush(self.heap, self.COMPARATOR(item, self.key))

    def __len__(self):
        return len(self.heap)


class MaxHeap(MinHeap):
    COMPARATOR = InverseComparator
