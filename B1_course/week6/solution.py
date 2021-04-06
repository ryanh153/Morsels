from collections import Counter
from sys import maxsize

import numpy as np


def average_age_under(people, max_age=maxsize):
    return np.mean([person['age'] for person in people if person['age'] < max_age])


def hobby_list(people):
    return [hobby for person in people for hobby in person['hobbies']]


def all_hobbies(people):
    return set(hobby_list(people))


def hobby_counter(people):
    return Counter(hobby_list(people))


def n_most_common(people, num):
    return [name for name, count in Counter(hobby_list(people)).most_common(num)]
