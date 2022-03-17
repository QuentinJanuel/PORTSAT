from pathlib import Path
from typing import List, Literal, Tuple
from utils.iccma.setup import setup

GraphType = Literal["gr", "st", "scc"]


def get_graphs(
    types: List[GraphType]
):
    setup()
    iccma15 = Path(__file__)\
        .parent\
        .joinpath("data")\
        .resolve()
    graphs: List[Tuple[Path, GraphType]] = []
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
            graphs.append((file, cur_type))
    return graphs
