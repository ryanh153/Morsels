from hashlib import md5
from pathlib import Path


class DirFileHash:

    def __init__(self, dir_path):
        self.dirname = dir_path
        self.dir_path = Path(dir_path)

    def __getitem__(self, item):
        if (file := self.dir_path.joinpath(item)).exists():
            return md5(open(file, 'rb').read()).hexdigest()
        return None
