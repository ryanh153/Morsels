import random


class RandomLooper:

    def __init__(self, *iterables):
        self.iterable = [i for iterable in iterables for i in iterable]

    def __iter__(self):
        shuffled = random.sample(self.iterable, len(self.iterable))
        yield from shuffled

    def __len__(self):
        return len(self.iterable)
