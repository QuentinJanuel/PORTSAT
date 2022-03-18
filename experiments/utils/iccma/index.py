from pathlib import Path
from typing import List
from utils.iccma.type import GraphType
from utils.iccma.setup import setup
from utils.iccma.iccma_graph import ICCMAGraph


def get_graphs(
    types: List[GraphType]
):
    setup()
    iccma15 = Path(__file__)\
        .parent\
        .joinpath("data")\
        .resolve()
    graphs: List["ICCMAGraph"] = []
    for dir in iccma15.iterdir():
        if "small" not in dir.name:
            continue
        cur_type: GraphType | None = None
        for type in types:
            if f"_{type}_" in dir.name:
                cur_type = type
                break
        if cur_type is None:
            continue
        for file in dir.iterdir():
            if file.suffix != ".tgf":
                continue
            graphs.append(ICCMAGraph(file, cur_type))
    return graphs
