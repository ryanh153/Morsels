import re

# def parse_ranges(input_str: str):
#     """Takes in a string containing intergers or ranges of intergers and returns an iterator that
#     iterates over all the numbers/range in the string. Ex: "1-3, 10, 11-13" yields 1,2,3,10,11,12,13"""
#     ranges = [x.strip() for x in input_str.split(',')]
#     for curr_range in ranges:
#         range_params = [x.strip() for x in curr_range.split('-')]
#         if len(range_params) == 2 and '>' not in range_params[1]:
#             yield from range(int(range_params[0]), int(range_params[1])+1)
#         else:
#             yield int(range_params[0])


def get_start_stop(group):
    """When passed a group (1-4, 4, 5->end, etc) get the first
    and last value that should be output to show range."""
    group = re.sub(r"->.*", r"", group)
    a, _, b = group.partition("-")
    return ((a, b) if b else (a, a))

def parse_ranges(input_str: str):
    """Takes in a string containing intergers or ranges of intergers and returns an iterator that
    iterates over all the numbers/range in the string. Ex: "1-3, 10, 11-13" yields 1,2,3,10,11,12,13"""
    return (
        num
        for group in input_str.split(",")
        for a, b in [get_start_stop(group)]
        for num in range(int(a), int(b)+1)
    )
