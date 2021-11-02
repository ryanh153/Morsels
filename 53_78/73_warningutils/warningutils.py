import warnings
from functools import wraps
import re


class error_on_warnings:
    def __init__(self, message='', category=Warning):
        self.message = message
        self.category = category

    def __enter__(self):
        warnings.filterwarnings('error', message=self.message, category=self.category)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        warnings.filters.pop(0)

    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return decorated


class NiceWarnings:

    def __init__(self, message, category):
        self.warning_list = list()
        self.message = message
        self.category = category

    def add_warning(self, warning):
        self.warning_list.append(warning)

    @property
    def results(self):
        caught_warnings = set()
        results = list()
        for warning in self.warning_list:
            if self.match(warning) and warning.category not in caught_warnings:
                results.append(NiceWarning(warning))
                caught_warnings.add(warning.category)

        return results

    def match(self, warning):
        return issubclass(warning.category, self.category) and bool(re.match(self.message, str(warning.message)))

    def __getitem__(self, index):
        return self.results[index]

    def __len__(self):
        return len(self.results)

    def __repr__(self):
        return f'[{", ".join([repr(warning) for warning in self.results])}]'


class NiceWarning:

    def __init__(self, warning):
        for name in dir(warning):
            if not name.startswith('_'):
                setattr(self, name, getattr(warning, name))

    def __repr__(self):
        return f'WarningMessage(message={self.message}, category={self.category}, ' \
               f'filename={self.filename}, lineno={self.lineno}'

class capture_warnings:

    contexts = list()

    def __init__(self, message='', category=Warning):
        self.message = message
        self.category = Warning
        self.original_msg_func = warnings._showwarnmsg_impl
        self.caught_warnings = NiceWarnings(message=message, category=category)

    def __enter__(self):
        warnings._showwarnmsg_impl = self.handle_warning
        self.contexts.append(self.caught_warnings)
        return self.caught_warnings

    def __exit__(self, exc_type, exc_val, exc_tb):
        warnings._showwarnmsg_impl = self.original_msg_func
        self.contexts.pop(-1)

    def handle_warning(self, warning):
        for context in self.contexts[::-1]:  # Search through contexts backwards through scopes
            if context.match(warning):  # Put in the deepest context it matches
                context.add_warning(warning)
                break
        else:  # If it doesn't match any context -> warn
            self.original_msg_func(warning)
