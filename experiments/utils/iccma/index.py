from pathlib import Path
from typing import List, Tuple
from utils.iccma.type import GraphType
from utils.iccma.setup import setup
from utils.iccma.type import Size
from utils.iccma.iccma_graph import ICCMAGraph


def get_graphs(
    selectors: List[Tuple[GraphType, Size]],
):
    setup()
    iccma15 = Path(__file__)\
        .parent\
        .joinpath("data")\
        .resolve()
    graphs: List["ICCMAGraph"] = []
    for dir in iccma15.iterdir():
        cur_type: GraphType | None = None
        for type, _ in selectors:
            if f"_{type}_" in dir.name:
                cur_type = type
                break
        if cur_type is None:
            continue
        cur_size: Size | None = None
        for _, size in selectors:
            if dir.name.endswith(f"_{size}"):
                cur_size = size
                break
        if cur_size is None:
            continue
        for file in dir.iterdir():
            if file.name.startswith("."):
                continue
            if file.suffix != ".tgf":
                continue
            graphs.append(ICCMAGraph(file, cur_type, cur_size))
    return graphs
