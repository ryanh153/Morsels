from hashlib import md5
from pathlib import Path


class DirFileHash:

    def __init__(self, dir_path):
        self.dir = Path(dir_path)

    def __getitem__(self, item):
        if (file := self.dir.joinpath(item)).exists():
            return md5(open(file, 'rb').read()).hexdigest()
        return None

    @property
    def dirname(self):
        return str(self.dir)
