from collections import Counter
from datetime import datetime, timedelta


def row_with_status(row, found):
    if found:
        return [*row, 'FOUND']
    else:
        return [*row, 'MISSING']

def surrounding(transaction):
    """Return the row key with date shifted by 1 on either side."""
    date_string, *rest = transaction
    date = datetime.strptime(date_string, '%Y-%m-%d').date()
    return [
        (str(date+timedelta(days=i)), *rest)
        for i in [-1, 0, 1]
    ]

def mark_transactions(to_search_for, search_in):
    """Return each row with appropriate FOUND/MISSING status added."""
    groups = Counter(search_in)
    matches = Counter()
    for row in sorted(to_search_for):
        for key in surrounding(row):
            if groups[key]:
                matches[row] += 1
                groups[key] -= 1
                break
    records = []
    for row in to_search_for:
        records.append(row_with_status(row, found=matches[row] > 0))
        matches[row] -= 1
    return records


def reconcile_accounts(transactions1, transactions2):
    """Return both transaction lists with FOUND/MISSING status added."""
    transactions1 = [tuple(r) for r in transactions1]
    transactions2 = [tuple(r) for r in transactions2]
    new1 = mark_transactions(transactions1, transactions2)
    new2 = mark_transactions(transactions2, transactions1)
    return new1, new2


records1 = [
            ['2017-05-02', 'A', '1.00', 'a'],
            ['2017-05-12', 'A', '5.00', 'a'],
            ['2017-04-30', 'A', '1.00', 'a'],
            ['2017-05-01', 'A', '1.00', 'a'],
]
records2 = [
    ['2017-05-13', 'A', '5.00', 'a'],
    ['2017-05-02', 'A', '1.00', 'a'],
    ['2017-05-01', 'A', '1.00', 'a'],
]

print(reconcile_accounts(records1, records2))