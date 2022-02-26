from pathlib import Path
from typing import List
from utils.test.setup import setup
from utils.test.tester import Tester


def get_testers(
    types: List[str]
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
        valid_type = False
        for type in types:
            if f"_{type}_" in dir.name:
                valid_type = True
                break
        if not valid_type:
            continue
        for file in dir.iterdir():
            if file.suffix != ".tgf":
                continue
            testers.append(Tester(file))
    return testers
