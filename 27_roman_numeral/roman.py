from functools import total_ordering
from itertools import zip_longest


@total_ordering
class RomanNumeral:
    symbols = {"M": 1000, "D": 500, "C": 100, "L": 50, "X": 10, "V": 5, "I": 1}
    builder = {"M": 1000, "CM": 900, "D": 500, "CD": 400, "C": 100, "XC": 90, "L": 50, "XL": 40, "X": 10, "IX": 9,
               "V": 5, "IV": 4, "I": 1}

    def __init__(self, string):
        self.string = string
        self.value = self._to_int()

    @classmethod
    def from_int(cls, num):
        chars = []
        for k, v in cls.builder.items():
            while num >= v:
                chars.append(k)
                num -= v
        return cls("".join(chars))

    def _to_int(self):
        total = 0
        nums = [self.symbols[c] for c in self.string]
        for num, next_num in zip_longest(nums, nums[1:], fillvalue=0):
            if num < next_num:
                total -= num
            else:
                total += num
        return total

    def __int__(self):
        return self.value

    def __str__(self):
        return self.string

    def __repr__(self):
        return f"{type(self).__name__}({self.string!r})"  # !r calls strings repr which adds the single quote around it

    def __add__(self, other):
        return RomanNumeral.from_int(int(self)+int(other))

    def __eq__(self, other):
        if isinstance(other, RomanNumeral):
            return int(self) == int(other)
        if isinstance(other, str):
            return self.string == other
        elif isinstance(other, int):
            return int(self) == other
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, RomanNumeral):
            return int(self) < int(other)
        elif isinstance(other, int):
            return int(self) < other
        else:
            return NotImplemented
