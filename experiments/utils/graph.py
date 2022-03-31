from io import TextIOWrapper
import os
from typing import Callable, Tuple, List
from utils.problem import Problem
from utils.iccma.iccma_graph import ICCMAGraph
from utils.problem import Semantics
from utils.solve import solve
from utils.iccma.ext_parser import parse_extensions
import networkx as nx
from pathlib import Path


class Graph:
    def __init__(
        self,
        vertices: List[str],
        edges: List[Tuple[str, str]] = [],
    ):
        self.vertices = vertices
        self.edges = edges

    def get_extensions(
        self,
        sem: Semantics,
        timeout: float | None = None,
    ) -> List[List[str]] | None:
        problem = Problem("EE", sem)
        result = solve(self, problem, timeout=timeout)
        if result is None:
            return None
        extensions = parse_extensions(result)
        return extensions

    def save(
        self,
        file_name: str,
        path: Path = Path("graph"),
    ) -> Tuple[Path, Path]:
        a = self.save_apx(file_name, path)
        b = self.save_tgf(file_name, path)
        return a, b

    def save_tgf(
        self,
        file_name: str,
        path: Path = Path("graph"),
    ) -> Path:
        def writer(f: TextIOWrapper):
            for v in self.vertices:
                f.write(f"{v}\n")
            f.write("#\n")
            for v1, v2 in self.edges:
                f.write(f"{v1} {v2}\n")
        return self._write(f"{file_name}.tgf", writer, path)

    def save_apx(
        self,
        file_name: str,
        path: Path = Path("graph"),
    ) -> Path:
        def writer(f: TextIOWrapper):
            for v in self.vertices:
                f.write(f"arg({v}).\n")
            for v1, v2 in self.edges:
                f.write(f"att({v1},{v2}).\n")
        return self._write(f"{file_name}.apx", writer, path)

    def _write(
        self,
        file_name: str,
        writer: Callable[[TextIOWrapper], None],
        path: Path,
    ) -> Path:
        if not os.path.exists(path):
            os.makedirs(path)
        file = path.joinpath(file_name)
        with open(file, "w") as f:
            writer(f)
        return file

    @staticmethod
    def from_iccma_graph(graph: ICCMAGraph):
        apx = graph\
            .get_input("apx")\
            .read_text()
        return Graph.from_apx(apx)

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
