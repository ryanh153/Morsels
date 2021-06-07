import re
import argparse
from pathlib import Path
from typing import Tuple, Generator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('re_str', type=str, help='String to search for')
    parser.add_argument('files', type=Path, nargs='+', help='File to search in')
    parser.add_argument('-i', '--ignore-case', action='store_true', help='Ignore case in search.')
    parser.add_argument('-n', '--line-number', action='store_true', help='Prepend line number to each printed line')
    parser.add_argument('-v', '--invert-match', action='store_true', help='Print un-matched instead of matched lines')
    parser.add_argument('-T', '--initial-tab', action='store_true', help='Put tab after line number')
    return parser.parse_args()


def search_file(re_str: str, file: Path, ignore_case: bool, add_line_number: bool, invert_matching: bool,
                initial_tab: bool) -> None:
    if not file.exists():
        raise ValueError(f'grep passed file that does not exist.\nPassed {file}')
    if ignore_case:
        re_str = re_str.lower()

    file_size = file.stat().st_size
    for line_number, (original, altered) in enumerate(iter_lines(file, ignore_case)):
        if should_display(altered, re_str, invert_matching):
            print_result(original, file, add_line_number, line_number, initial_tab, file_size)


def should_display(string: str, re_str: str, invert_matching: bool) -> bool:
    if not invert_matching:
        return re.search(re_str, string) is not None
    return re.search(re_str, string) is None


def iter_lines(file: Path, ignore_case: bool) -> Generator[Tuple[str, str], None, None]:
    with open(file, 'r') as f:
        for line in f:
            yield (line, line.lower()) if ignore_case else (line, line)


def print_result(string: str, file: Path, add_line_number: bool, line_number: int, initial_tab: bool, file_size: int)\
        -> None:
    file_expression = file if add_line_number else ''
    line_expression = line_number if add_line_number else ''
    spacer = get_spacer(initial_tab, add_line_number, file_size)
    print(f'{file_expression}{spacer}{line_expression}{spacer}{string}', end='')


def get_spacer(initial_tab: bool, add_line_number: bool, file_size: int) -> str:
    if not (initial_tab and add_line_number):
        return ''
    return ''.join([' ' for _ in range(len(str(file_size))-1)])


if __name__ == '__main__':
    args = parse_args()
    for file_to_parse in args.files:
        search_file(args.re_str, file_to_parse, args.ignore_case, args.line_number, args.invert_match, args.initial_tab)
        print('', flush=True)
