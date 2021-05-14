from random import randint


class RandMemory:
    """Takes in a max/min value
    Generates random numbers in that range (inclusive)
    Stores the history of numbers generated"""

    def __init__(self, lowest, highest):
        self._lowest = lowest
        self._highest = highest
        self._result_log = list()

    @property
    def lowest(self):
        return self._lowest

    @property
    def highest(self):
        return self._highest

    @property
    def get(self):
        """Get a new number and log it"""
        self._result_log.append(randint(self.lowest, self.highest))
        return self._result_log[-1]

    def history(self):
        """Return list of logged numbers"""
        return self._result_log
