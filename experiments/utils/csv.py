from typing import Any, List
from utils.benchmark.export import Export
import pandas as pd


class CSV:
    def __init__(self):
        self._has_template = False
        self._rows: List[List[str]] = []

    def add_row(self, *args: Any) -> None:
        row = [str(arg) for arg in args]
        self._rows.append(row)

    def template(self, *args: Any) -> None:
        if self._has_template:
            raise Exception(" ".join([
                "Cannot set the template because",
                "this csv has already been templated",
            ]))
        self.add_row(*args)
        self._has_template = True

    def save(self, name: str, export: Export):
        file = f"{export.get_file_name(name)}.csv"
        df = pd.DataFrame(self._rows)
        df.to_csv(file, index=False, header=False)
