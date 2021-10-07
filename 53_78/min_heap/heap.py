import heapq


class MinHeap:

    def __init__(self, iterable, key=lambda x: x):
        self.key = key
        self.heap = [val for val in iterable]
        self._sort_heap()

    def _sort_heap(self):
        self.heap = sorted(self.heap, key=self.key, reverse=True)

    def peek(self):
        return self.heap[-1]

    def pop(self):
        return self.heap.pop()

    def push(self, item):
        self.heap.append(item)
        self._sort_heap()

    def __len__(self):
        return len(self.heap)


class MaxHeap(MinHeap):

    def _sort_heap(self):
        self.heap = sorted(self.heap, key=self.key, reverse=False)


## Real
# import heapq
# import heapq_max
#
#
# class MinHeap:
#
#     def __init__(self, iterable, key=lambda x: x):
#         # Copy data and store comparable value and original value as the first and second items in a tuple
#         self.heap = [(key(val), val) for val in iterable]
#         heapq.heapify(self.heap)
#         self.key = key
#
#     def peek(self):
#         return heapq.nsmallest(1, self.heap)[0][1]
#
#     def pop(self):
#         return heapq.heappop(self.heap)[1]
#
#     def push(self, item):
#         heapq.heappush(self.heap, (self.key(item), item))
#
#     def __len__(self):
#         return len(self.heap)
#
#
# class MaxHeap:
#
#     def __init__(self, iterable, key=lambda x: x):
#         # Copy data and store comparable value and original value as the first and second items in a tuple
#         self.heap = [(key(val), val) for val in iterable]
#         heapq_max.heapify_max(self.heap)
#         self.key = key
#
#     def peek(self):
#         return heapq.nlargest(1, self.heap)[0][1]
#
#     def pop(self):
#         return heapq_max.heappop_max(self.heap)[1]
#
#     def push(self, item):
#         heapq_max.heappush_max(self.heap, (self.key(item), item))
#
#     def __len__(self):
#         return len(self.heap)

