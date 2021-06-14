import re
import argparse
from typing import TextIO, Pattern
import os


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('re_str', type=str, help='String to search for')
    parser.add_argument('files', type=argparse.FileType('rt'), nargs='+', help='File to search in')
    parser.add_argument('-i', '--ignore-case', action='store_const', const=re.I, default=0, dest='flags',
                        help='Ignore case in search.')
    parser.add_argument('-n', '--line-number', action='store_true', help='Prepend line number to each printed line')
    parser.add_argument('-v', '--invert-match', action='store_true', help='Print un-matched instead of matched lines')
    parser.add_argument('-T', '--initial-tab', action='store_true', help='Put tab after line number')
    return parser.parse_args()


def search_file(file: TextIO, compiled_re: Pattern[str], add_line_number: bool, show_filename: bool,
                invert_matching: bool, initial_tab: bool) -> None:

    file_size = get_file_size(file)

    for line_number, line in enumerate(file):
        if bool(compiled_re.search(line)) != invert_matching:
            print_result(line, file, add_line_number, line_number, show_filename, initial_tab, file_size)


def get_file_size(file: TextIO) -> int:
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    return file_size


def print_result(string: str, file: TextIO, add_line_number: bool, line_number: int, show_filename: bool,
                 initial_tab: bool, file_size: int) -> None:
    file_expression = f'{file.name}:' if show_filename else ''
    file_spacer = '\t' if initial_tab and show_filename else ''

    # Converting to string and get length -> gives number of digits in number
    line_number_width = len(str(file_size))+1 if initial_tab else 0
    line_expression = f'{line_number+1}:'.rjust(line_number_width, ' ') if add_line_number else ''
    line_spacer = '\t' if initial_tab else ''

    print(f'{file_expression}{file_spacer}{line_expression}{line_spacer}{string.rstrip(os.linesep)}')


def get_spacer(initial_tab: bool, add_line_number: bool, file_size: int) -> str:
    if not (initial_tab and add_line_number):
        return ''
    return ''.join([' ' for _ in range(len(str(file_size))-1)])


if __name__ == '__main__':
    args = parse_args()
    re_comp = re.compile(args.re_str, flags=args.flags)
    display_filename = len(args.files) > 1
    for file_to_parse in args.files:
        search_file(file_to_parse, re_comp, args.line_number, display_filename, args.invert_match, args.initial_tab)
