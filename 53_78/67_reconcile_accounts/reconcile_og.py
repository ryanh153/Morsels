import datetime


FOUND, MISSING = 'FOUND', 'MISSING'
format_str = '%Y-%m-%d'
secs_per_day = 3600*24


def reconcile_accounts(data1, data2):
    entries_per_line = len(data1[0]) if len(data1) else 0
    remaining_set = [([el for el in sublist], index) for index, sublist in enumerate(data2)]
    data1, sort_indices = sort_data1_with_memory(data1)
    out1, out2 = [[el for el in sublist] for sublist in data1], [[el for el in sublist] for sublist in data2]

    for i, row1 in enumerate(data1):
        index, remaining_set = get_best_match(row1, remaining_set)
        if index is not None:
            out1[i].append(FOUND)
            out2[index].append(FOUND)

    for i, row1 in enumerate(out1):
        if len(row1) == entries_per_line:
            out1[i].append(MISSING)

    for j, row2 in enumerate(out2):
        if len(row2) == entries_per_line:
            out2[j].append(MISSING)

    final_out = [[] for _ in out1]
    for i, index in enumerate(sort_indices):
        final_out[i] = out1[index]
    return final_out, out2


def sort_data1_with_memory(data1):
    initial_data_with_ordering = [([el for el in sublist], index) for index, sublist in enumerate(data1)]
    sorted_input_with_ordering = sorted(initial_data_with_ordering,
                                        key=lambda entry: datetime.datetime.strptime(entry[0][0], format_str))
    return [entry[0] for entry in sorted_input_with_ordering], [entry[1] for entry in sorted_input_with_ordering]


def get_best_match(entry, possible_matches):
    out_indices, in_indices, separations = list(), list(), list()
    for ii, (row2, oi) in enumerate(possible_matches):
        if entry[1::] == row2[1::]:
            time_sep = dates_close(entry[0], row2[0])
            if abs(time_sep) <= 1:
                out_indices.append(oi), separations.append(time_sep), in_indices.append(ii)

    remove_match_index = None if not len(in_indices)\
        else [i for i, s in zip(in_indices, separations) if s == min(separations)][0]
    if remove_match_index is not None:
        possible_matches.pop(remove_match_index)
    # Index on the output array where our match was found
    found_match_index = None if not len(out_indices)\
        else [i for i, s in zip(out_indices, separations) if s == min(separations)][0]
    return found_match_index, possible_matches


def dates_close(date_str1, date_str2):
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
#
# # records1, records2 = list(), list()
#
print(reconcile_accounts(records1, records2))
