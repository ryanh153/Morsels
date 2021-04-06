import unicodedata
from abc import ABC, abstractmethod
from collections import UserString
from functools import total_ordering


def normalize_caseless(text):
    return unicodedata.normalize("NFKD", text.casefold())


@total_ordering
class TotalOrder(ABC):
    @abstractmethod
    def __eq__(self, other):
        """Abstract. Child must define"""
    def __lt__(self, other):
        """Abstract: Child must define"""


class FuzzyString(TotalOrder, UserString):

    def __eq__(self, other):
        if isinstance(other, str):
            return normalize_caseless(self.data) == normalize_caseless(other)

    def __lt__(self, other):
        if isinstance(other, str):
            return normalize_caseless(self.data) < normalize_caseless(other)

    def __contains__(self, item):
        if isinstance(item, str):
            return normalize_caseless(item) in normalize_caseless(self.data)
