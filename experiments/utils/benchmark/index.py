from typing import List
from utils.iccma.index import get_graphs, GraphType
from utils.benchmark.tester import Tester


def get_testers(
    types: List[GraphType]
):
    graphs = get_graphs(types)
    testers: List["Tester"] = []
    for graph in graphs:
        file_name = graph[0]
        type = graph[1]
        testers.append(Tester(file_name, type))
    return testers
