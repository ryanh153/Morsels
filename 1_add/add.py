def get_shape(my_list):
    """Returns a list of the length of each sublist in a 2D list"""
    return [len(row) for row in my_list]


def add(*lists):
    """Add an arbitrary number of 2D lists"""
    first_shape = get_shape(lists[0])
    if any(first_shape != get_shape(curr_list) for curr_list in lists[1::]):
        raise ValueError("Unequel list sizes!")
    return [[sum(values) for values in zip(*rows)] for rows in zip(*lists)]


# def add(*lists):
#     if any([len(row) for row in lists[0]] != [len(row) for row in curr_list] for curr_list in lists[1::]):
#         raise ValueError("Unequel list sizes!")
#     return [[sum(values) for values in zip(*rows)] for rows in zip(*lists)]
