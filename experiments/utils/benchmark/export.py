from pathlib import Path


class Export:
    def __init__(self, path: Path, prefix: str = ""):
        self._path: Path = path
        self._prefix: str = prefix
        self._path.mkdir(parents=True, exist_ok=True)

    def get_file_name(self, name: str):
        full_name = name
        if len(self._prefix) > 0:
            full_name = f"{self._prefix}_{name}"
        return self._path.joinpath(full_name)
