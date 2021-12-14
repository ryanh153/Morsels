# from argparse import ArgumentParser
# from pathlib import Path
# import os
# import re
#
#
# def scan(pattern, filename):
#     # cover and special characters in the pattern
#     pattern = re.escape(pattern)
#     # Find the capture groups in the pattern as specified
#     matches = re.finditer('%[a-zA-Z0-9]', pattern)
#     # Keys are the letter after the % symbol
#     keys = [match.group()[1] for match in matches]
#     # Make a pattern from the one given with capture groups
#     subbed = re.sub('%[A-Z]', f'([^/]+?)', pattern)  # Anything but slash (conservative)
#     subbed = re.sub('%[a-z]', f'([^/ ]+?)', subbed)  # Anything but slash or spaces (conservative)
#     subbed = re.sub('%[0-9]', '([0-9]+)', subbed) + '$'  # Any integers (greedily)
#     # Try and match the pattern with capture groups
#     post = re.match(subbed, filename)
#     if post is None:  # If there are no matches return None
#         return None
#     # Otherwise construct a dictionary from the keys and captured data
#     d = {key: value for key, value in zip(keys, post.groups())}
#     return d
#
#
# def format(format_str, data):
#     # Check that every required key is in the data dictionary
#     keys_needed = re.finditer('%[A-Z]', format_str)
#     for match in keys_needed:
#         if f'{match.group()[1]}' not in data:
#             raise KeyError(f'{match.group()[1]} in dictionary but not in format string ( {format_str} )')
#
#     # Make a regex that searches for any of the data dictionary keys
#     regex = re.compile('(' + '|'.join([f'%{key}' for key in data]) + ')')
#     # Fill in the format_str with the value in the data dictionary at the key from each match
#     return regex.sub(lambda match_object: data[match_object.group()[1]], format_str)
#
#
# def parse_args():
#     parser = ArgumentParser()
#     parser.add_argument('input_format', type=str)
#     parser.add_argument('output_format', type=str)
#     parsed = parser.parse_args()
#     return parsed.input_format, parsed.output_format
#
#
# if __name__ == '__main__':
#     input_format, output_format = parse_args()
#     for file in Path('.').glob('**/*'):
#         if file.is_file():
#             input_file_str = str(file)
#             file_data = scan(input_format, input_file_str)
#             if file_data is not None:
#                 output_file_str = format(output_format, file_data)
#                 print(f'Moving \"{input_file_str}\" to \"{output_file_str}\"')
#
#
from glob import glob
import re


def scan(pattern, filename):
    pattern = re.escape(pattern)
    def sub(m):
        """Return named group with appropriate regex in it."""
        c = m.group(1)
        if c.isdigit():
            regex = r"\d+"
        elif c.islower():
            regex = r"[^\\/ ]+?"
        else:
            regex = r"[^\\/]+?"
        return fr"(?P<G{c}>{regex})"
    regex = re.sub(r'%(\w)', sub, pattern)
    match = re.fullmatch(regex, filename)
    if match:
        return {
            k: v
            for (_, k), v in match.groupdict().items()
        }  # Remove G before each group name
    return None


def format(pattern, data):
    format_string = re.sub(r'%(\w)', r'%(\1)s', pattern)
    return format_string % data


def find_files(pattern):
    pattern = re.sub(r'\*', r'\*', pattern)
    return glob(re.sub(r'%(\w)', r'*', pattern))


def main(from_pattern, to_pattern):
    for filename in find_files(from_pattern):
        parts = scan(from_pattern, filename)
        if parts is not None:
            destination = format(to_pattern, parts)
            print("Moving", f'"{filename}"', "to", f'"{destination}"')


if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])