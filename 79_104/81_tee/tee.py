import sys
from argparse import ArgumentParser
from pathlib import Path


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('out_paths', nargs='*', type=Path, default=Path('out.txt').resolve(),
                        help='Name of file to write captured output to')
    parser.add_argument('-a', '--append_mode', action='store_true', help='Write to files in append mode')
    parsed = parser.parse_args()
    paths = [parsed.out_paths.resolve()] if isinstance(parsed.out_paths, Path) \
        else [path.resolve() for path in parsed.out_paths]
    return paths, parsed.append_mode


if __name__ == '__main__':
    out_paths, append_bool = parse_args()
    text = b''.join(line for line in sys.stdin.buffer.readlines())
    try:
        text = text.decode('ascii')
        binary = False
        write_type = 'a' if append_bool else 'w'
    except UnicodeDecodeError:
        binary = True
        write_type = 'ab' if append_bool else'wb'

    for out_path in out_paths:
        with open(out_path, write_type) as f:
            f.write(text)

    if binary:
        sys.stdout.buffer.write(text)
    else:
        sys.stdout.write(text)
