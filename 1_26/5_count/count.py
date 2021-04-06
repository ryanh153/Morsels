import re
from collections import Counter


def count_words(input_str):
    """Count number of occurences of each word in input."""
    return Counter(re.findall(r"\w[\w'-]*\w|\w", input_str.lower()))
