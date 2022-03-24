from io import TextIOWrapper
import os
from typing import Callable, Tuple, List
import networkx as nx


class Graph:
    def __init__(
        self,
        vertices: List[str],
        edges: List[Tuple[str, str]] = [],
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

    @staticmethod
    def from_apx(apx: str) -> "Graph":
        vertices = []
        edges = []
        for line in apx.split("\n"):
            if line.startswith("arg("):
                vertices.append(line[4:-2])
            if line.startswith("att("):
                a1, a2 = line[4:-2].split(",")
                edges.append((a1, a2))
        return Graph(vertices, edges)

    @staticmethod
    def from_networkx(nx_graph: nx.Graph) -> "Graph":
        return Graph(
            [n for n in nx_graph.nodes],
            [e for e in nx_graph.edges],
        )
