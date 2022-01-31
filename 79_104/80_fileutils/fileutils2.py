import os
import hashlib
from collections import defaultdict, Counter


def find_duplicates(files):
    results = defaultdict(list)
    size_list = [os.path.getsize(file) for file in files]
    sizes = Counter(size_list)
    for file, size in zip(files, size_list):
        if sizes[size] > 1:
            with open(file, 'rb') as f:
                data_str = ''.join(str(line) for line in f.readlines()).encode('utf-8')
            results[hashlib.md5(data_str).hexdigest()].append(file)
    return [file_list for file_list in results.values() if len(file_list) > 1]
