#!/usr/bin/env python3

from collections import Counter

import pytest
import solution

all_people = [{'name': 'Reuven', 'age': 50, 'hobbies': ['Python', 'cooking', 'reading']},
              {'name': 'Atara', 'age': 20, 'hobbies': [
                  'horses', 'cooking', 'art', 'reading']},
              {'name': 'Shikma', 'age': 18, 'hobbies': [
                  'Python', 'piano', 'cooking', 'reading']},
              {'name': 'Amotz', 'age': 15, 'hobbies': ['boxing', 'cooking']}]


@pytest.mark.parametrize('people, maxage, output', [
    ({}, 120, 0),
    (all_people, 120, 23.25),
    (all_people, 25, 17.6666),
    (all_people, -1, 0)
])
def test_average_age_under(people, maxage, output):
    assert pytest.approx(solution.average_age_under(people, maxage), output)


@pytest.mark.parametrize('people, output', [
    ({}, set()),
    (all_people, {'Python', 'reading', 'horses',
     'art', 'piano', 'cooking', 'boxing'})
])
def test_all_hobbies(people, output):
    assert solution.all_hobbies(people) == output


@pytest.mark.parametrize('people, output', [
    ({}, Counter()),
    (all_people, Counter({'Python': 2, 'boxing': 1, 'cooking': 4,
     'art': 1, 'horses': 1, 'piano': 1, 'reading': 3}))
])
def test_hobby_counter(people, output):
    assert solution.hobby_counter(people) == output


@pytest.mark.parametrize('people, n, output', [
    ({}, 3, []),
    (all_people, 3, ['Python', 'reading', 'cooking'])
])
def test_n_most_common(people, n, output):
    assert sorted(solution.n_most_common(people, 3)) == sorted(output)