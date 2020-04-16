import argparse
import csv
import sys


COLUMN_TYPES = {'str': str, 'num': float}


def process_column_sort(column_string):
    try:
        number, type_string = column_string.split(':')
    except ValueError:
        number, type_string = column_string, 'str'
    n = int(number)
    try:
        python_type = COLUMN_TYPES[type_string]
    except KeyError:
        raise ValueError(f"Unknown column type specified: {type_string}")
    return n, python_type


def typed_index_key(columns):
    def key_func(row):
        return [
            type_(row[index])
            for index, type_ in columns
        ]
    return key_func


def main(args):
    reader = csv.reader(args.csv_file)
    writer = csv.writer(sys.stdout)
    if args.with_header:
        writer.writerow(next(reader))
    writer.writerows(sorted(reader, key=typed_index_key(args.columns)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file', type=argparse.FileType(mode='rt'))
    parser.add_argument('columns', nargs='+', type=process_column_sort)
    parser.add_argument('--with-header', action='store_true')
    main(parser.parse_args())