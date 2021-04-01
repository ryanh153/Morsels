import numpy as np
from collections import Counter
from sys import maxsize


def average_age_under(people, max_age=maxsize):
    return np.mean([d['age'] for d in people if d['age'] < max_age])


def hobby_list(people):
    return [hobby for d in people for hobby in d['hobbies']]


def all_hobbies(people):
    return set(hobby_list(people))


def hobby_counter(people):
    return Counter(hobby_list(people))


def n_most_common(people, num):
    return [item[0] for item in Counter(hobby_list(people)).most_common(num)]
