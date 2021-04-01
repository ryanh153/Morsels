import numpy as np
from collections import Counter


def average_age_under(people, max_age=None):
    return np.mean([d['age'] for d in people if (max_age is None or d['age'] < max_age)])


def hobby_list(people):
    return [hobby for d in people for hobby in d['hobbies']]


def all_hobbies(people):
    return set(hobby_list(people))


def hobby_counter(people):
    return Counter(hobby_list(people))


def n_most_common(people, num):
    return [res[0] for res in Counter(hobby_list(people)).most_common(num)]
