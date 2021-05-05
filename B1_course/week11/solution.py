from hashlib import md5
from pathlib import Path


class DirFileHash:

    def __init__(self, dir_path):
        self.dirname = dir_path
        self.dir_path = Path(dir_path)

    def __getitem__(self, item):
        file = self.dir_path.joinpath(item)
        if file.exists():
            return md5(open(file, 'rb').read()).hexdigest()
        return None
