import csv
from collections import defaultdict
from itertools import zip_longest


def csv_columns(file_obj, headers=None, missing=None):
    reader = csv.reader(file_obj, delimiter=',', quotechar='"')
    if headers is None:
        headers = next(reader)
    return {
        header: list(data)
        for header, *data in zip_longest(headers, *reader, fillvalue=missing)
    }


def csv_columns_dict_reader(file_obj, headers=None, missing=None):
    reader = csv.DictReader(file_obj, fieldnames=headers, restval=missing, delimiter=',', quotechar='"')
    result = defaultdict(list)
    for row in reader:
        for header, value in row.items():
            result[header].append(value)
    return result
