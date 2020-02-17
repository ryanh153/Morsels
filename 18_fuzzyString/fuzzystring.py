import unicodedata


def normalize_caseless(text):
    return unicodedata.normalize("NFKD", text.casefold())


class FuzzyString(str):

    def __eq__(self, other):
        if isinstance(other, str):
            return normalize_caseless(self) == normalize_caseless(other)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, str):
            return normalize_caseless(self) < normalize_caseless(other)
        else:
            raise TypeError("Other must be of type string to compare to FuzzyString")

    def __gt__(self, other):
        if isinstance(other, str):
            return normalize_caseless(self) > normalize_caseless(other)
        else:
            raise TypeError("Other must be of type string to compare to FuzzyString")

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __contains__(self, item):
        if isinstance(item, str):
            return normalize_caseless(item) in normalize_caseless(self)
        else:
            return False

    def __add__(self, other):
        if isinstance(other, str):
            return FuzzyString(str(self) + str(other))
        else:
            raise TypeError("Other must be of type string to compare to FuzzyString")
