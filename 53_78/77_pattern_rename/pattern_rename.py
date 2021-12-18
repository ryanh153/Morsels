from argparse import ArgumentParser
import re
from glob import glob


def scan(pattern, filename):
    # cover and special characters in the pattern
    pattern = re.escape(pattern)
    # Find the capture groups in the pattern as specified
    matches = re.finditer('%[a-zA-Z0-9]', pattern)
    # Keys are the letter after the % symbol
    keys = [match.group()[1] for match in matches]
    # Make a pattern from the one given with capture groups
    subbed = re.sub('%[A-Z]', r'([^\\/]+?)', pattern)  # Anything but slash (conservative)
    subbed = re.sub('%[a-z]', r'([^\\/ ]+?)', subbed)  # Anything but slash or spaces (conservative)
    subbed = re.sub('%[0-9]', '([0-9]+)', subbed)  # Any integers (greedily)
    # Try and match the pattern with capture groups
    post = re.fullmatch(fr'{subbed}', fr'{filename}')
    if post is None:  # If there are no matches return None
        return None
    # Otherwise construct a dictionary from the keys and captured data
    d = {key: value for key, value in zip(keys, post.groups())}
    return d


def format(format_str, data):
    # Check that every required key is in the data dictionary
    keys_needed = re.finditer('%[A-Z]', format_str)
    for match in keys_needed:
        if f'{match.group()[1]}' not in data:
            raise KeyError(f'{match.group()[1]} in dictionary but not in format string ( {format_str} )')

    # Make a regex that searches for any of the data dictionary keys
    regex = re.compile('(' + '|'.join([f'%{key}' for key in data]) + ')')
    # Fill in the format_str with the value in the data dictionary at the key from each match
    return regex.sub(lambda match_object: data[match_object.group()[1]], format_str)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('input_format', type=str)
    parser.add_argument('output_format', type=str)
    parsed = parser.parse_args()
    return parsed.input_format, parsed.output_format


if __name__ == '__main__':
    input_format, output_format = parse_args()
    for file in glob(re.sub(r'%\w', r'*', input_format)):
        file_data = scan(input_format, file)
        if file_data is not None:
            output_file_str = format(output_format, file_data)
            print(f'Moving \"{file}\" to \"{output_file_str}\"')
