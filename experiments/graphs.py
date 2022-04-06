from utils.graph import Graph
import networkx as nx
from utils.benchmark.inputs import Inputs, frange
from typing import TypedDict, Callable


class GraphT(TypedDict):
    x_label: str
    inputs: Inputs
    gen: Callable[[float], Graph]


graphs: dict[str, GraphT] = {
    "complete": {
        "x_label": "#nodes",
        "inputs": Inputs(frange(1, 500, 15)),
        "gen": lambda n: Graph.from_nx_gen(nx.complete_graph(n)),
    },
    "cycle": {
        "x_label": "#nodes",
        "inputs": Inputs(frange(1000, 10000, 100)),
        "gen": lambda n: Graph.from_nx_gen(nx.cycle_graph(n)),
    },
    "barbell_path_100": {
        "x_label": "#nodes per complete graph",
        "inputs": Inputs(frange(1, 1000, 10)),
        "gen": lambda m1: Graph.from_nx_gen(
            nx.barbell_graph(m1, 100)
        ),
    },
    "barbell_size_100": {
        "x_label": "path length",
        "inputs": Inputs(frange(1, 100, 10)),
        "gen": lambda m2: Graph.from_nx_gen(
            nx.barbell_graph(100, m2)
        ),
    },
    "binomial_tree": {
        "x_label": "order",
        "inputs": Inputs(frange(1, 100, 10)),
        "gen": lambda n: Graph.from_nx_gen(nx.binomial_tree(n)),
    },
    "circular_ladder": {
        "x_label": "length",
        "inputs": Inputs(frange(1, 100, 10)),
        "gen": lambda n: Graph.from_nx_gen(
            nx.circular_ladder_graph(n)
        ),
    },
    "dorogovtsev_goltsev_mendes": {
        "x_label": "generation",
        "inputs": Inputs(frange(1, 100, 10)),
        "gen": lambda n: Graph.from_nx_gen(
            nx.dorogovtsev_goltsev_mendes_graph(n)
        ),
    },
    "ladder": {
        "x_label": "length",
        "inputs": Inputs(frange(1, 100, 10)),
        "gen": lambda n: Graph.from_nx_gen(nx.ladder_graph(n)),
    },
    "path": {
        "x_label": "length",
        "inputs": Inputs(frange(1, 100, 10)),
        "gen": lambda n: Graph.from_nx_gen(nx.path_graph(n)),
    },
    "star": {
        "x_label": "length",
        "inputs": Inputs(frange(1, 100, 10)),
        "gen": lambda n: Graph.from_nx_gen(nx.star_graph(n)),
    },
    "wheel": {
        "x_label": "cycle length",
        "inputs": Inputs(frange(1, 100, 10)),
        "gen": lambda n: Graph.from_nx_gen(nx.wheel_graph(n)),
    },
    "margulis_gabber_galil": {
        "x_label": "sqrt(#nodes)",
        "inputs": Inputs(frange(1, 100, 10)),
        "gen": lambda n: Graph.from_nx_gen(
            nx.margulis_gabber_galil_graph(n)
        ),
    },
    "hypercube": {
        "x_label": "dimension",
        "inputs": Inputs(frange(1, 100, 10)),
        "gen": lambda n: Graph.from_nx_gen(nx.hypercube_graph(n)),
    },
    "gn": {
        "x_label": "#nodes",
        "inputs": Inputs(frange(1, 100, 10)),
        "gen": lambda n: Graph.from_nx_gen(nx.gn_graph(n)),
    },
    "gnc": {
        "x_label": "#nodes",
        "inputs": Inputs(frange(1, 100, 10)),
        "gen": lambda n: Graph.from_nx_gen(nx.gnc_graph(n)),
    },
    "scale_free": {
        "x_label": "#nodes",
        "inputs": Inputs(frange(1, 100, 10)),
        "gen": lambda n: Graph.from_nx_gen(nx.scale_free_graph(n)),
    },
    "navigable_small_world": {
        "x_label": "sqrt(#nodes)",
        "inputs": Inputs(frange(1, 100, 10)),
        "gen": lambda n: Graph.from_nx_gen(
            nx.navigable_small_world_graph(n)
        ),
    },
    "waxman": {
        "x_label": "#nodes",
        "inputs": Inputs(frange(1, 100, 10)),
        "gen": lambda n: Graph.from_nx_gen(nx.waxman_graph(n)),
    },
    "random_internet": {
        "x_label": "#nodes",
        "inputs": Inputs(frange(1000, 10000, 100)),
        "gen": lambda n: Graph.from_nx_gen(
            nx.random_internet_as_graph(n)
        ),
    },
    "random_tree": {
        "x_label": "#nodes",
        "inputs": Inputs(frange(1000, 10000, 100)),
        "gen": lambda n: Graph.from_nx_gen(nx.random_tree(n)),
    },
    "mycielski": {
        "x_label": "order",
        "inputs": Inputs(frange(1, 1000, 10)),
        "gen": lambda n: Graph.from_nx_gen(nx.mycielski_graph(n)),
    },
    "random_cograph": {
        "x_label": "order",
        "inputs": Inputs(frange(1, 1000, 10)),
        "gen": lambda n: Graph.from_nx_gen(nx.random_cograph(n)),
    },
    "sudoku": {
        "x_label": "order",
        "inputs": Inputs(frange(1, 1000, 10)),
        "gen": lambda n: Graph.from_nx_gen(nx.sudoku_graph(int(n))),
    },
}
