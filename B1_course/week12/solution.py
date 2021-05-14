from random import randint
from typing import List


class RandMemory:
    """Takes in a max/min value
    Generates random numbers in that range (inclusive)
    Stores the history of numbers generated"""

    def __init__(self, lowest: int, highest: int) -> None:
        self._lowest = lowest
        self._highest = highest
        self._result_log: List[int] = list()

    @property
    def lowest(self) -> int:
        return self._lowest

    @property
    def highest(self) -> int:
        return self._highest

    @property
    def get(self) -> int:
        """Get a new number and log it"""
        self._result_log.append(randint(self.lowest, self.highest))
        return self._result_log[-1]

    def history(self) -> List[int]:
        """Return list of logged numbers"""
        return self._result_log
