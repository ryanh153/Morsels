from pathlib import Path


def file_func(dir_path, func):
    dir_path = validate_dir(dir_path)
    successes, fails = dict(), dict()
    for file in dir_path.iterdir():
        try:
            successes[file] = func(file)
        except Exception as e:
            fails[file] = e

    return successes, fails


def validate_dir(dir_path):
    if not (isinstance(dir_path, str) or isinstance(dir_path, Path)):
        raise ValueError('Directory path must be string or Path object')

    dir_path = Path(dir_path)
    if not dir_path.is_dir():
        raise ValueError(f'{dir_path} is not a directory')

    return dir_path
