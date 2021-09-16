from collections import Counter
from datetime import datetime, timedelta


def reconcile_accounts(transactions1, transactions2):
    # Make counters (need to pass tuples since they will be dict keys)
    transactions1 = [tuple(entry) for entry in transactions1]
    transactions2 = [tuple(entry) for entry in transactions2]

    final1 = check_entries(transactions1, transactions2)
    final2 = check_entries(transactions2, transactions1)

    return final1, final2


def check_entries(check_for, check_in):
    counter = Counter(check_in)
    with_indices = sorted([(entry, i) for i, entry in enumerate(check_for)])
    time_sorted = [list(check_entry(entry[0], counter)) for entry in with_indices]
    final = [entry for entry in time_sorted]
    for curr_index, (_, goal_index) in enumerate(with_indices):
        final[goal_index] = time_sorted[curr_index]
    return final


def check_entry(key, counter):
    for time_key in make_keys_for_time_search(key):
        if time_key in counter and counter[time_key] > 0:
            counter[time_key] -= 1
            return *key, 'FOUND'
    else:
        return *key, 'MISSING'


def make_keys_for_time_search(key):
    fmt = '%Y-%m-%d'
    before = (datetime.strptime(key[0], fmt) + timedelta(days=-1)).strftime(fmt)
    after = (datetime.strptime(key[0], fmt) + timedelta(days=1)).strftime(fmt)
    return (before, *key[1::]), key, (after, *key[1::])
