import pickle
from pathlib import Path


def load(path: Path):
    with open(path, 'rb') as f:
        return pickle.load(f)


def save(obj, path: Path):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)
