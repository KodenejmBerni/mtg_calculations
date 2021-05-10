import json
from pathlib import Path
from urllib.request import urlopen

import pkl_module


class CardDB:
    db_paths = set()

    def __new__(cls, db_path: Path):
        if db_path in cls.db_paths:
            raise PathInUse
        cls.db_paths.add(db_path)
        return super().__new__(cls)

    def __init__(self, db_path: Path):
        assert db_path.suffix == '.json'
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.path = db_path
        self.data = None

    def __del__(self):
        self.db_paths.remove(self.path)

    def update(self, url: str):
        with urlopen(url) as response:
            self.data = json.load(response)
        pkl_module.save(self.data, self.path)

    def load(self):
        self.data = pkl_module.load(self.path)


class PathInUse(Exception):
    pass
