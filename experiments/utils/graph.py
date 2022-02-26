from io import TextIOWrapper
import os
from typing import Callable, Tuple, List


class Graph:
    def __init__(
        self,
        vertices: List[int],
        edges: List[Tuple[int, int]] = [],
    ):
        self.vertices = vertices
        self.edges = edges

    def save(self, file_name: str):
        self.save_apx(file_name)
        self.save_tgf(file_name)

    def save_tgf(self, file_name: str):
        def writer(f: TextIOWrapper):
            for v in self.vertices:
                f.write(f"{v}\n")
            f.write("#\n")
            for v1, v2 in self.edges:
                f.write(f"{v1} {v2}\n")
        self._write(f"{file_name}.tgf", writer)

    def save_apx(self, file_name: str):
        def writer(f: TextIOWrapper):
            for v in self.vertices:
                f.write(f"arg({v}).\n")
            for v1, v2 in self.edges:
                f.write(f"att({v1},{v2}).\n")
        self._write(f"{file_name}.apx", writer)

    def _write(
        self,
        file_name: str,
        writer: Callable[[TextIOWrapper], None],
    ):
        if not os.path.exists("graph"):
            os.makedirs("graph")
        with open(f"graph/{file_name}", "w") as file:
            writer(file)
