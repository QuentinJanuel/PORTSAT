from pathlib import Path
from typing import List, Literal
from utils.test.setup import setup
from utils.test.tester import Tester


def get_testers(
    types: List[Literal["gr", "st", "scc"]]
):
    setup()
    iccma15 = Path(__file__)\
        .parent\
        .joinpath("iccma15")\
        .resolve()
    testers: List["Tester"] = []
    for dir in iccma15.iterdir():
        if "small" not in dir.name:
            continue
        cur_type: Literal["gr", "st", "scc"] | None = None
        for type in types:
            if f"_{type}_" in dir.name:
                cur_type = type
                break
        if cur_type is None:
            continue
        for file in dir.iterdir():
            if file.suffix != ".tgf":
                continue
            testers.append(Tester(file, cur_type))
    return testers
