import json
import pickle
from datetime import datetime
from urllib.request import urlopen
from pathlib import Path





card_db_metadata_path = Path('card_db_metadata.pkl')
if card_db_metadata_path.exists():
    with open(card_db_metadata_path, 'rb') as f:
        card_db_metadata = pickle.load(f)
else:
    pass
with urlopen('https://api.scryfall.com/bulk-data') as response:
    bulk_data = json.load(response)
    now = datetime.utcnow()
