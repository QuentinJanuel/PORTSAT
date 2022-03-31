from statistics import mean
from typing import Callable, List, Sequence
from utils.graph import Graph
from utils.benchmark.benchmark import benchmark_solve
from utils.benchmark.randomized_executor import RandomizedExecutor, Job
from utils.benchmark.get_args import GetArgs
from utils.benchmark.timeouts import Timeouts
from utils.benchmark.export import Export
from utils.problem import Problem
from itertools import product
from pathlib import Path
import matplotlib.pyplot as plt  # type: ignore


def bench(
    x_label: str,
    inputs: Sequence[float],
    graph_generator: Callable[[float], Graph],
    solvers: List[str],
    problem: Problem,
    timeout: float,
    name: str = "my_graph",
    export: Export = Export(Path("results")),
    repetitions: int = 1,
):
    time_lists: dict[str, dict[float, float]] = {
        solver: {}
        for solver in solvers
    }
    timeouts = Timeouts(timeout)
    executor = RandomizedExecutor[float]()
    for param, _ in product(inputs, range(repetitions)):
        graph = graph_generator(param)
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
                executor.add(f"{param}{solver}", job)
    executor.exec_all()
    for param, solver in product(inputs, solvers):
        results = executor.get_results(f"{param}{solver}")
        for secs in results:
            timeouts.new_result(solver, secs)
        time_lists[solver][param] = mean(results)
    save_graph(
        name,
        x_label,
        time_lists,
        export,
    )


def save_graph(
    name: str,
    x_label: str,
    time_lists: dict[str, dict[float, float]],
    export: Export,
):
    _, ax = plt.subplots()
    for solver, time_list in time_lists.items():
        x = list(time_list.keys())
        y = list(time_list.values())
        ax.plot(x, y, label=solver)
    ax.set_title(name)
    ax.set_xlabel(x_label)
    ax.set_ylabel("Time (s)")
    ax.legend()
    plt.savefig(
        f"{export.get_file_name(name)}.png",
        facecolor="white",
        transparent=False,
        bbox_inches="tight",
    )
    plt.close()


def frange(start: float, stop: float, step: float) -> Sequence[float]:
    seq = []
    i = start
    while i < stop:
        seq.append(i)
        i += step
    return seq
