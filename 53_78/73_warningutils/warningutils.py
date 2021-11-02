import contextlib
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

    def __init__(self, warning_list, message, category):
        self.warning_list = warning_list
        self.message = message
        self.category = category

    @property
    def unmatched_results(self):
        return [NiceWarning(warning) for warning in self.warning_list
                if not self.match(warning)]

    @property
    def results(self):
        return [NiceWarning(warning) for warning in self.warning_list
                if self.match(warning)]

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
        self.warning = warning
        for name in dir(warning):
            if not name.startswith('_'):
                setattr(self, name, getattr(warning, name))

    def __repr__(self):
        return f'WarningMessage(message={self.message}, category={self.category}, ' \
               f'filename={self.filename}, lineno={self.lineno}'


@contextlib.contextmanager
def capture_warnings(message='', category=Warning):
    with warnings.catch_warnings(record=True) as warnings_list:
        nice_warnings = NiceWarnings(warnings_list, message, category)
        yield nice_warnings
    for warning in nice_warnings.unmatched_results:
        warnings.warn(warning.warning)
