import argparse
import re
from tokenize import tokenize
from token import STRING


concat_re = re.compile(r'([\'\"]) .+? \1 \s*? ([\'\"]) .+? \2', re.VERBOSE)
multi_re = re.compile(r'( ([\'\"]) .+? \2 \s* ([\'\"]) .+? \3 )', re.VERBOSE)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+', help='Files to have concat check run on')
    args = parser.parse_args()

    for file in args.files:
        # print(file)
        prev_type = None
        for tk_data in tokenize(open(file, 'rb').readline):
            # print(f'token with row {tk_data.start[0]} and type {tk_data.type}. The value is\n{tk_data.string}')
            if prev_type == tk_data.type == STRING:
                print(f'{file}, line {tk_data.start[0]}: implicit concatenation')
            prev_type = tk_data.type
        # error_lines = []
        # for i, line in enumerate(open(file, 'r').readlines()):
        #     if concat_re.findall(line) and i not in error_lines:
        #         print(f'{file}, line {i+1}: implicit concatenation')
        #         error_lines.append(i)
        #
        # all_lines = list(open(file, 'r').readlines())
        # joined = ''.join(all_lines)
        # multi_find = multi_re.findall(joined)
        # if multi_find:
        #     print(multi_find)
        #     for i, line in enumerate(all_lines):
        #         for captured in multi_find:
        #             # print(f'checking if {line.strip()} is in {captured[0]}')
        #             if line.strip() in captured[0].split('\n')[0] and i not in error_lines:
        #                 print(f'{file}, line {i + 1}: implicit concatenation (multi)')
        #                 error_lines.append(i)
