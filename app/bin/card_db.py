import json
from pathlib import Path
from urllib.request import urlopen
import numpy as np
from bin.utils import pkl_module


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
        self.data = {}

    def __del__(self):
        self.db_paths.remove(self.path)

    def update(self, url: str) -> None:
        with urlopen(url) as response:
            data = json.load(response)
            self.data = self._remote_db_to_local_db(data)
        pkl_module.save(self.data, self.path)

    def load(self) -> None:
        self.data = pkl_module.load(self.path)

    def exists(self) -> bool:
        return self.path.exists()

    def find_card(self, card_name: str) -> dict:
        return self.data[card_name]

    @staticmethod
    def _remote_db_to_local_db(remote_data: list[dict]) -> dict[str]:
        # 1st filter: tokens, no img, misc
        data_filtered_1 = []
        for card in remote_data:
            try:
                assert 'Token' not in card['type_line']
                assert card['type_line'] != 'Card'
                assert card['image_status'] != 'missing'
                data_filtered_1.append(card)
            except AssertionError:
                pass

        # 2nd filter: cards with duplicated name
        all_names = [card['name'] for card in data_filtered_1]
        unique_names, unique_counts = np.unique(all_names, return_counts=True)
        duplicate_names = unique_names[unique_counts > 1]
        data_filtered_2 = filter(lambda x: x['name'] not in duplicate_names, data_filtered_1)

        # Build
        local_data = {}
        for card in sorted(data_filtered_2, key=lambda x: x['name']):
            if 'image_uris' in card:
                front_image_url = card['image_uris']['normal'],
                back_image_url = None
            else:
                front_image_url = card['card_faces'][0]['image_uris']['normal']
                back_image_url = card['card_faces'][1]['image_uris']['normal']
            local_data[card['name']] = {
                'front_image_url': front_image_url,
                'back_image_url': back_image_url,
            }
        return local_data


class PathInUse(Exception):
    pass
