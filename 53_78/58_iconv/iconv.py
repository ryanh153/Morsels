from argparse import ArgumentParser, FileType


def main():
    args = ArgumentParser()
    args.add_argument('input', nargs='?', default='-', type=FileType('rt'))  # basically an already open file?
    args.add_argument('-o', '--output', default='-', type=FileType('wt'))  # '-' is the default for stdin/stdout
    args.add_argument('-t', '--to-code')
    args.add_argument('-f', '--from-code')
    args.add_argument('-c', dest='errors', action='store_const', const='ignore', default='strict')
    parsed = args.parse_args()

    parsed.input.reconfigure(encoding=parsed.from_code, errors=parsed.errors)
    parsed.output.reconfigure(encoding=parsed.to_code)

    for line in parsed.input:
        parsed.output.write(line)


if __name__ == '__main__':
    """Note: The tests for this fail to due an encoding issue I cannot figure out. They all pass online"""
    main()
