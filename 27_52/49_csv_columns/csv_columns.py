from itertools import zip_longest
import csv


def csv_columns(file_obj, headers=None, missing=None):
    reader = csv.reader(file_obj, delimiter=',', quotechar='"')
    if headers is None:
        headers = next(reader)
    result = {h: [] for h in headers}
    for line in reader:
        for key, val in zip_longest(headers, line, fillvalue=missing):
            result[key].append(val)
    return result
