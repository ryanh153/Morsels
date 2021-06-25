import datetime


FOUND, MISSING = 'FOUND', 'MISSING'
format_str = '%Y-%m-%d'
secs_per_day = 3600*24


def reconcile_accounts(data1, data2):
    entries_per_line = len(data1[0]) if len(data1) else 0
    remaining_set = [([el for el in sublist], index) for index, sublist in enumerate(data2)]
    out1, out2 = [[el for el in sublist] for sublist in data1], [[el for el in sublist] for sublist in data2]

    for i, row1 in enumerate(data1):
        index = get_best_match(row1, remaining_set)
        if index is not None:
            remaining_set.remove((row1, index))
            out1[i].append(FOUND)
            out2[index].append(FOUND)

    for i, row1 in enumerate(out1):
        if len(row1) == entries_per_line:
            out1[i].append(MISSING)

    for j, row2 in enumerate(out2):
        if len(row2) == entries_per_line:
            out2[j].append(MISSING)

    return out1, out2


def get_best_match(entry, possible_matches):
    # print(possible_matches)
    indices, separations = list(), list()
    for row2, index in possible_matches:
        # print(f'{entry}\n{row2}\n\n')
        if (entry[1::] == row2[1::]) and (entry in [r[0] for r in possible_matches]):
            time_sep = dates_close(entry[0], row2[0])
            if time_sep <= 1:
                indices.append(index), separations.append(time_sep)

    return None if not len(indices) else [i for i, s in zip(indices, separations) if s == min(separations)][0]


def dates_close(date_str1, date_str2):
    # print(date_str1)
    date1 = datetime.datetime.strptime(date_str1, format_str)
    date2 = datetime.datetime.strptime(date_str2, format_str)
    return (date1-date2).days


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

# records1, records2 = list(), list()

print(reconcile_accounts(records1, records2))