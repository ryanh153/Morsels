# def deep_flatten(source_iter):
#     """Accepts an iterable of iterables (ex: list of lists) and flattens it recursively."""
#     for inner_iter in source_iter:
#         try:
#             iter(inner_iter)
#         except TypeError:  # not iterable -> single element -> yield
#             yield inner_iter
#         else:  # iterable
#             if isinstance(inner_iter, str):  # don't breakdown strings -> yield
#                 yield inner_iter
#             else:  # iterable -> flatten it -> yield each item in order
#                 yield from deep_flatten(inner_iter)

# Another option if you're ok with requiring iterables to be an instance of collections.abc.Iterable
from collections.abc import Iterable


def deep_flatten(source_iter):
    """Accepts an iterable of iterables (ex: list of lists) and flattens it recursively."""
    for inner_iter in source_iter:
        if not isinstance(inner_iter, Iterable) or isinstance(inner_iter, str):
            yield inner_iter
        else:  # iterable
            yield from deep_flatten(inner_iter)
