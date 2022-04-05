from utils.graph import Graph
import networkx as nx
from utils.benchmark.line_graph import bench, frange


networkXDict={
        "complete_graph":
        {

            "name":"complete",
            "x_label":"nodes",
            "inputs":frange(1, 1000, 10),
            "graph_generator":lambda n: Graph.from_nx_gen(nx.complete_graph(n)),
            "nbParams":1
        },
        "cycle_graph":
        {
            "name":"cycle",
            "x_label":"nodes",
            "inputs":frange(1000,10000,100),
            "graph_generator":lambda n: Graph.from_nx_gen(nx.cycle_graph(n)),
            "nbParams":1
        },
        "barbell_graph":
        {
            "name":"barbell_path",
            "x_label":"nodes per complete graph",
            "inputs":frange(1, 1000, 10),
            "graph_generator":lambda m1: Graph.from_nx_gen(nx.barbell_graph(m1, 100)),
            "nbParams":1
        },
        "binomial_tree":
        {
            "name":"binomial_tree",
            "x_label":"Order of the binomial tree",
            "inputs":frange(1, 100, 10),
            "graph_generator":lambda n: Graph.from_nx_gen(nx.binomial_tree(n)),
            "nbParams":1
        },
        "circular_ladder_graph":
        {
            "name":"circular_ladder_graph",
            "x_label":"n pairs of concentric nodes",
            "inputs":frange(1, 100, 10),
            "graph_generator":lambda n: Graph.from_nx_gen(nx.circular_ladder_graph(n)),
            "nbParams":1,
        },
        "dorogovtsev_goltsev_mendes_graph":
        {
            "name":"dorogovtsev_goltsev_mendes_graph",
            "x_label":"n is the generation",
            "inputs":frange(1, 100, 10),
            "graph_generator":lambda n: Graph.from_nx_gen(nx.dorogovtsev_goltsev_mendes_graph(n)),
            "nbParams":1,
        },
        "ladder_graph":
        {
            "name":"ladder_graph",
            "x_label":"length n",
            "inputs":frange(1, 100, 10),
            "graph_generator":lambda n: Graph.from_nx_gen(nx.ladder_graph(n)),
            "nbParams":1,
        },
        "path_graph":
        {
            "name":"path_graph",
            "x_label":"length n",
            "inputs":frange(1, 100, 10),
            "graph_generator":lambda n: Graph.from_nx_gen(nx.path_graph(n)),
            "nbParams":1,
        },
        "star_graph":
        {
            "name":"star_graph",
            "x_label":"length n",
            "inputs":frange(1, 100, 10),
            "graph_generator":lambda n: Graph.from_nx_gen(nx.star_graph(n)),
            "nbParams":1,
        },
        "wheel_graph":
        {
            "name":"wheel_graph",
            "x_label":"cycle of (n-1) nodes",
            "inputs":frange(1, 100, 10),
            "graph_generator":lambda n: Graph.from_nx_gen(nx.wheel_graph(n)),
            "nbParams":1,
        },
        "margulis_gabber_galil_graph":
        {
            "name":"margulis_gabber_galil_graph",
            "x_label":"nodes",
            "inputs":frange(1, 100, 10),
            "graph_generator":lambda n: Graph.from_nx_gen(nx.margulis_gabber_galil_graph(n)),
            "nbParams":1,
        },
        "hypercube_graph":
        {
            "name":"hypercube_graph",
            "x_label":"nodes",
            "inputs":frange(1, 100, 10),
            "graph_generator":lambda n: Graph.from_nx_gen(nx.hypercube_graph(n)),
            "nbParams":1,
        },

        "gn_graph":
        {
            "name":"gn_graph",
            "x_label":"nodes",
            "inputs":frange(1, 100, 10),
            "graph_generator":lambda n: Graph.from_nx_gen(nx.gn_graph(n)),
            "nbParams":1,
        },

        "gnc_graph":
        {
            "name":"gnc_graph",
            "x_label":"nodes",
            "inputs":frange(1, 100, 10),
            "graph_generator":lambda n: Graph.from_nx_gen(nx.gnc_graph(n)),
            "nbParams":1,
        },
        "scale_free_graph":
        {
            "name":"scale_free_graph",
            "x_label":"nodes",
            "inputs":frange(1, 100, 10),
            "graph_generator":lambda n: Graph.from_nx_gen(nx.scale_free_graph(n)),
            "nbParams":1,
        },
        "navigable_small_world_graph":
        {
            "name":"navigable_small_world_graph",
            "x_label":"nodes",
            "inputs":frange(1, 100, 10),
            "graph_generator":lambda n: Graph.from_nx_gen(nx.navigable_small_world_graph(n)),
            "nbParams":1,
        },
        "waxman_graph":
        {
            "name":"waxman_graph",
            "x_label":"nodes",
            "inputs":frange(1, 100, 10),
            "graph_generator":lambda n: Graph.from_nx_gen(nx.waxman_graph(n)),
            "nbParams":1,
        },
        "random_internet_as_graph":
        {
            "name":"random_internet_as_graph",
            "x_label":"nodes",
            "inputs":frange(1000, 10000, 100),
            "graph_generator":lambda n: Graph.from_nx_gen(nx.random_internet_as_graph(n)),
            "nbParams":1,
        },
        "random_tree":
        {
            "name":"random_tree",
            "x_label":"nodes",
            "inputs":frange(1000, 10000, 100),
            "graph_generator":lambda n: Graph.from_nx_gen(nx.random_tree(n)),
            "nbParams":1,
        },
        "mycielski_graph":
        {
            "name":"mycielski_graph",
            "x_label":"nodes",
            "inputs":frange(1, 1000, 10),
            "graph_generator":lambda n: Graph.from_nx_gen(nx.mycielski_graph(n)),
            "nbParams":1,
        },
        "random_cograph":
        {
            "name":"random_cograph",
            "x_label":"nodes",
            "inputs":frange(1, 1000, 10),
            "graph_generator":lambda n: Graph.from_nx_gen(nx.random_cograph(n)),
            "nbParams":1,
        },
        "sudoku_graph":
        {
            "name":"sudoku_graph",
            "x_label":"nodes",
            "inputs":frange(1, 1000, 10),
            "graph_generator":lambda n: Graph.from_nx_gen(nx.sudoku_graph(n)),
            "nbParams":1,
        }


}