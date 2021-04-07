from pathlib import Path


def file_func(dir_path, func):
    dir_path = validate_dir(dir_path)
    successes, fails = dict(), dict()
    for file in dir_path.glob('*'):
        try:
            successes[file] = func(file)
        except Exception as e:
            fails[file] = e

    return successes, fails


def validate_dir(dir_path):
    if not (isinstance(dir_path, str) or isinstance(dir_path, Path)):
        raise ValueError('Directory path must be string or Path object')

    directory = Path(dir_path)
    if not directory.is_dir():
        raise ValueError(f'{dir_path} is not a directory')

    return directory
