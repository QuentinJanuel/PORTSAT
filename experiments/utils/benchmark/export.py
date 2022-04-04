from pathlib import Path
from typing import List


class Export:
    def __init__(self, path: Path, prefix: str = ""):
        self._path: Path = path
        self._path.mkdir(parents=True, exist_ok=True)
        self._prefixes: List[str] = []
        self._suffixes: List[str] = []
        self.add_prefix(prefix)

    def add_prefix(self, prefix: str):
        if len(prefix) > 0:
            self._prefixes.append(prefix)

    def add_suffix(self, suffix: str):
        if len(suffix) > 0:
            self._suffixes.append(suffix)

    def get_file_name(self, name: str):
        full_name = "_".join([
            *self._prefixes,
            name,
            *self._suffixes,
        ])
        return self._path.joinpath(full_name)
