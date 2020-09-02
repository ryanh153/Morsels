import argparse
from tokenize import tokenize
from token import STRING, NL


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+', help='Files to have concat check run on')
    args = parser.parse_args()

    for file in args.files:
        prev_string, prev_type, prev_row = None, None, None
        for tk_data in tokenize(open(file, 'rb').readline):
            if prev_type == tk_data.type == STRING:
                print(f'{file}, line {prev_row} between {prev_string} and {tk_data.string}')
            if tk_data.type != NL:  # don't update on new line to catch multi-line implicit concatenation
                prev_string, prev_type, prev_row = tk_data.string, tk_data.type,  tk_data.end[0]
