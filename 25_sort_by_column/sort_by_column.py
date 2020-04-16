import argparse
import csv
import sys
from functools import partial


def my_sort(row, cols, type_calls):
    """Make tuple that will be used for sorting. Tuple is col element of row for col in cols"""
    return [type_call(row[col]) for col, type_call in zip(cols, type_calls)]


def process_column(col_str):
    try:
        col, type_call = col_str.split(":")
        return [int(col), str] if type_call == "str" else [int(col), float]
    except ValueError:
        return int(col_str), str


if __name__ == "__main__":
    # Parse inputs
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType('r'))
    parser.add_argument("cols", type=str, nargs='+')
    parser.add_argument("--with-header", action="store_true")
    args = parser.parse_args()
    # two lists (cols and type_calls) type_calls is a list of callables
    cols, type_calls = zip(*[process_column(col) for col in args.cols])
    # Get reader and writer (that writes to stdout)
    reader = csv.reader(args.file, delimiter=',', quotechar='"')
    writer = csv.writer(sys.stdout, delimiter=',', quotechar='"')
    # use writer to print data
    if args.with_header:  # if we have a header write it first
        writer.writerow(next(reader))
    writer.writerows(sorted(reader, key=partial(my_sort, cols=cols, type_calls=type_calls)))
