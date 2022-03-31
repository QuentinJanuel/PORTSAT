from statistics import mean
from typing import Dict, List
from utils.graph import Graph
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
    graphs: List[Graph],
    solvers: List[str],
    semantics: List[Semantics],
    tasks: List[Task],
    timeout: float,
    name: str = "my_graph",
    export: Export = Export(Path("results")),
    repetitions: int = 1,
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
    executor = RandomizedExecutor[float](repetitions)
    for problem, graph in product(problems, graphs):
        get_args = GetArgs(graph, problem)
        for solver in solvers:
            for arg in get_args.get():
                job = Job[float](
                    benchmark_solve,
                    graph=graph,
                    problem=problem,
                    solvers=[solver],
                    arg=arg,
                    timeout=timeout,
                )
                executor.add(f"{solver};{problem}", job)
    executor.exec_all()
    for solver, problem in product(solvers, problems):
        results = executor.get_results(f"{solver};{problem}")
        for secs in results:
            timeouts.new_result(solver, secs)
        stats[f"{solver};{problem}"] = mean(results)
    executor.get_df().to_csv(f"{export.get_file_name(name)}.csv")
    save_graph(name, solvers, stats, problems, timeouts, export)


def save_graph(
    name: str,
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
            stats[f"{solver};{p}"]
            for p in labels
        ]
        ax.bar(
            x - total_width / 2 + width * (i + .5),
            solver_means,
            width,
            label=solver,
        )
    ax.set_title(name)
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
        f"{export.get_file_name(name)}.png",
        facecolor="white",
        transparent=False,
        bbox_inches="tight",
    )
    plt.close()
