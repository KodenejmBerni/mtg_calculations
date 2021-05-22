import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

from bin.utils import pkl_module
from bin.card_db import CardDB


class DBManager:
    metadata_url = 'https://api.scryfall.com/bulk-data'
    remote_db_name = 'Oracle Cards'
    remote_db_timestamp = None
    remote_db_url = None
    manager_dirs = set()
    manager_dbs = set()

    def __new__(cls, manager_dir: Path, card_db: CardDB):
        if manager_dir in cls.manager_dirs:
            raise DirInUse
        if card_db in cls.manager_dbs:
            raise DBInUse
        cls.manager_dirs.add(manager_dir)
        cls.manager_dbs.add(card_db)
        return super().__new__(cls)

    def __init__(self, manager_dir: Path, card_db: CardDB):
        manager_dir.mkdir(parents=True, exist_ok=True)
        self.dir = manager_dir
        self.config_path = manager_dir / 'config.pkl'
        self.db = card_db
        self.last_db_update = None

    def __del__(self):
        self.manager_dirs.remove(self.dir)
        self.manager_dbs.remove(self.db)

    def is_update_available(self):
        self.update_remote_info()
        if self.last_db_update is None:
            return True
        return self.remote_db_timestamp > self.last_db_update

    def db_update(self):
        self.db.update(self.remote_db_url)
        self.last_db_update = datetime.now(timezone.utc)

    def db_exists(self):
        return self.db.exists()

    def db_load(self):
        self.db.load()

    def config_exists(self) -> bool:
        return self.config_path.exists()

    def config_load(self):
        config = pkl_module.load(self.config_path)
        self.last_db_update = config['last_db_update']

    def config_save(self):
        config = {
            'last_db_update': self.last_db_update,
        }
        pkl_module.save(config, self.config_path)

    @classmethod
    def update_remote_info(cls):
        with urlopen(cls.metadata_url) as response:
            metadata = json.load(response)
        for el in metadata['data']:
            if el['name'] == cls.remote_db_name:
                cls.remote_db_timestamp = datetime.fromisoformat(el['updated_at'])
                cls.remote_db_url = el['download_uri']
                break
        else:
            raise KeyError(f'No "{cls.remote_db_name}" DB found in metadata.')


class DirInUse(Exception):
    pass


class DBInUse(Exception):
    pass
