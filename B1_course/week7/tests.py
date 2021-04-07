import os
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from solution import file_func


# Helper functions
def file_length(filename):
    return os.stat(filename).st_size


def accept_files(filename):
    if filename.is_dir():
        raise ValueError(f'{filename} is not a file! is_dir returns {filename.is_dir()}')


def fill_with_text_files(directory, num_files=5):
    files = list()
    for i in range(num_files):
        files.append(directory / f'temp_file{i}.txt')
        files[-1].write_text(''.join(['Hello!' for _ in range(i)]))
    return files


def fill_with_files_and_directories(directory, num_files=5, num_dirs=5):
    contents = list()
    for i in range(num_files):
        contents.append(directory / f'temp_file{i}.txt')
        contents[-1].write_text(''.join(['Hello!' for _ in range(i)]))

    for i in range(num_dirs):
        contents.append(directory / f'temp_dir{i}')
        contents[-1].mkdir()

    return contents


# Tests
def test_empty_directory():
    with TemporaryDirectory() as temp_dir:
        success_dict, fail_dict = file_func(temp_dir, file_length)
        assert type(success_dict) == dict
        assert type(fail_dict) == dict
        assert len(success_dict) == 0
        assert len(fail_dict) == 0


def test_invalid_directory():
    invalid_directory = Path('not/a/path')
    pytest.raises(ValueError, file_func, invalid_directory, lambda x: x)
    invalid_path_type = None
    pytest.raises(ValueError, file_func, invalid_path_type, lambda x: x)


def test_str_and_path_inputs():
    with TemporaryDirectory() as dir_str:
        dir_path = Path(dir_str)
        fill_with_files_and_directories(dir_path)
        success_dict_str, fail_dict_str = file_func(dir_str, file_length)
        success_dict_path, fail_dict_path = file_func(dir_path, file_length)
        assert success_dict_str == success_dict_path
        assert fail_dict_str == fail_dict_path


def test_single_empty_file():
    with TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        num_files = 1
        files = fill_with_text_files(temp_dir, num_files)
        success_dict, fail_dict = file_func(str(temp_dir), file_length)
        assert len(success_dict) == num_files
        assert len(fail_dict) == 0
        for index, file in enumerate(files):
            assert success_dict[file] == 0


def test_length_of_text_files():
    with TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        num_files = 5
        size_of_word = 6  # size of file with the word 'hello' in it
        files = fill_with_text_files(temp_dir, num_files)
        success_dict, fail_dict = file_func(str(temp_dir), file_length)
        assert len(success_dict) == num_files
        assert len(fail_dict) == 0
        for index, file in enumerate(files):
            assert success_dict[file] == index*size_of_word


def test_with_failures():
    with TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        num_files, num_dirs = 3, 2
        fill_with_files_and_directories(temp_dir, num_files=num_files, num_dirs=num_dirs)
        success_dict, fail_dict = file_func(str(temp_dir), accept_files)
        assert len(success_dict) == num_files
        assert len(fail_dict) == num_dirs
