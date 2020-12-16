from argparse import ArgumentParser
import sys
from io import TextIOWrapper


def main():
    args = ArgumentParser()
    args.add_argument('input', nargs='?', default='-')
    args.add_argument('-o', '--output', required=False, default=None)
    args.add_argument('-t', '--to-code', required=False, default=None)
    args.add_argument('-f', '--from-code', required=False, default=None)
    args.add_argument('-c', action='store_true', help='Ignore encoding errors')
    parsed = args.parse_args()

    if parsed.input == '-':
        if parsed.c:
            in_file = TextIOWrapper(sys.stdin.buffer, encoding=parsed.from_code, errors='ignore')
        else:
            in_file = TextIOWrapper(sys.stdin.buffer, encoding=parsed.from_code)
        lines = [line for line in in_file]
    elif parsed.c:
        in_file = open(parsed.input, mode='rb')
        lines = [in_file.read().decode(parsed.from_code, errors='ignore')]
    else:
        in_file = open(parsed.input, mode='r+', encoding=parsed.from_code)
        lines = [line for line in in_file]

    if parsed.output is None:
        output_file = TextIOWrapper(sys.stdout.buffer, encoding=parsed.to_code)
    else:
        output_file = open(parsed.output, mode='w', encoding=parsed.to_code)

    with output_file as of:
        with in_file:
            for line in lines:
                of.write(line)


if __name__ == '__main__':
    """Note: The tests for this fail to due an encoding issue I cannot figure out. They all pass online"""
    main()
