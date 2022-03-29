from statistics import mean
from typing import Dict, List
from utils.graph import Graph
from utils.iccma.iccma_graph import ICCMAGraph
from utils.benchmark.benchmark import benchmark_solve
from utils.benchmark.randomized_executor import RandomizedExecutor, Job
from utils.benchmark.timeouts import Timeouts
from utils.benchmark.export import Export
from utils.benchmark.get_args import GetArgs
from utils.problem import Task, Semantics, Problem
from itertools import product
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt  # type: ignore


def bench(
    iccma_graphs: List[ICCMAGraph],
    solvers: List[str],
    semantics: List[Semantics],
    tasks: List[Task],
    timeout: float,
    export: Export = Export(Path("results"), ""),
):
    """
    Generates a benchmark graph for the given graphs, solvers and semantics.

    Parameters :
    ------------
    graphs: the graphs to benchmark
    solvers: the solvers to benchmark
    semantics: the semantics to benchmark
    tasks: the tasks to benchmark
    timeout: the timeout to use for the benchmark
    export: (optional) sets where to export the graph

    Example :
    ---------
    >>> bench(
    ...     graphs=get_graphs([("scc", "medium")]),
    ...     solvers=["minisat", "manysat"],
    ...     semantics=["PR"],
    ...     tasks=["SE"],
    ...     timeout=10 * 60,
    ... )
    """
    stats: Dict[str, float] = {}
    problems: List[Problem] = [
        Problem(task, sem)
        for task, sem in product(tasks, semantics)
    ]
    timeouts = Timeouts(timeout)
    executor = RandomizedExecutor[float]()
    for problem, iccma_graph in product(problems, iccma_graphs):
        graph = Graph.from_iccma_graph(iccma_graph)
        get_args = GetArgs(graph, problem)
        for solver in solvers:
            for arg in get_args.get():
                job = Job[float](
                    benchmark_solve,
                    input=iccma_graph.get_input(),
                    problem=problem,
                    solvers=[solver],
                    arg=arg,
                    timeout=timeout,
                )
                executor.add(f"{solver}{problem}", job)
    executor.exec_all()
    for solver, problem in product(solvers, problems):
        results = executor.get_results(f"{solver}{problem}")
        for secs in results:
            timeouts.new_result(solver, secs)
        stats[f"{solver}{problem}"] = mean(results)
    save_graph(iccma_graphs, solvers, stats, problems, timeouts, export)


def save_graph(
    iccma_graphs: List[ICCMAGraph],
    solvers: List[str],
    stats: Dict[str, float],
    problems: List[Problem],
    timeouts: Timeouts,
    export: Export,
):
    labels = [str(p) for p in problems]
    x = np.arange(len(labels))
    width = 1 / (len(solvers) + 1)
    total_width = width * len(solvers)
    fig, ax = plt.subplots()
    for i, solver in enumerate(solvers):
        solver_means = [
            stats[f"{solver}{p}"]
            for p in labels
        ]
        ax.bar(
            x - total_width / 2 + width * (i + .5),
            solver_means,
            width,
            label=solver,
        )
    ax.set_title(get_title(iccma_graphs))
    ax.set_ylabel("Time (s)")
    ax.set_xticks(x, labels)
    fig.text(
        0.5,
        0.01,
        str(timeouts),
        wrap=True,
        horizontalalignment="right",
        verticalalignment="top",
        fontsize=12,
    )
    ax.legend()
    plt.savefig(
        f"{export.get_file_name(ax.get_title())}.png",
        facecolor="white",
        transparent=False,
        bbox_inches="tight",
    )
    plt.close()


def get_title(iccma_graphs: List["ICCMAGraph"]) -> str:
    categories = [f"{g.get_type()}-{g.get_size()}" for g in iccma_graphs]
    return ", ".join([*{*categories}])
