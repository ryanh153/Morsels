def deep_flatten(source_iter):
    """Accepts an iterable of iterables (ex: list of lists) and flattens it recursively."""
    for inner_iter in source_iter:
        try:
            iter(inner_iter)
        except TypeError:  # not iterable -> single element -> yield
            yield inner_iter
        else:  # iterable
            if isinstance(inner_iter, str):  # don't breakdown strings -> yield
                yield inner_iter
            else:  # iterable -> flatten it -> yield each item in order
                result = deep_flatten(inner_iter)
                for item in result:
                    yield item
