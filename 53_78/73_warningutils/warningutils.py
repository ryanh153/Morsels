from contextlib import contextmanager
from dataclasses import dataclass
import re
import warnings


@contextmanager
def error_on_warnings(message='', category=Warning):
    with warnings.catch_warnings():
        warnings.filterwarnings('error', message, category)
        yield


@dataclass
class NiceWarning:
    message: Warning
    category: type
    filename: str
    lineno: int


@contextmanager
def capture_warnings(message='', category=Warning):
    regex = re.compile(message)
    target_category = category

    def log_warnings(message_to_log, category_to_log, filename, lineno, *args, **kwargs):
        if regex.match(str(message_to_log)) and issubclass(category_to_log, target_category):
            logs.append(NiceWarning(message_to_log, category_to_log, filename, lineno))
        else:
            showwarning(message_to_log, category_to_log, filename, lineno, *args, **kwargs)

    logs = []
    showwarning = warnings.showwarning
    warnings.showwarning = log_warnings
    try:
        yield logs
    finally:
        warnings.showwarning = showwarning
