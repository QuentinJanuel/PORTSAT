from statistics import mean
from typing import Callable, List, Sequence
from utils.csv import CSV
from utils.graph import Graph
from utils.benchmark.benchmark import benchmark_solve
from utils.benchmark.randomized_executor import RandomizedExecutor, Job
from utils.benchmark.get_args import GetArgs
from utils.benchmark.timeouts import Timeouts
from utils.benchmark.export import Export
from utils.problem import Problem
from utils.progress import Progress
from itertools import product
from pathlib import Path
import matplotlib.pyplot as plt  # type: ignore


def bench(
    x_label: str,
    inputs: Sequence[float],
    graph_generator: Callable[[float], Graph],
    solvers: List[str],
    problem: Problem,
    name: str,
    timeout: float = 10 * 60,  # 10 minutes
    export: Export | None = None,
    repetitions: int = 1,
):
    if export is None:
        export = Export(Path("results"))
    export.add_suffix(str(problem))
    time_lists: dict[str, dict[float, float]] = {
        solver: {}
        for solver in solvers
    }
    timeouts = Timeouts(timeout)
    executor = RandomizedExecutor[float]()
    progress = Progress("Generation", len(inputs) * repetitions)
    for gen_cur, (param, _) in enumerate(product(inputs, range(repetitions))):
        graph = graph_generator(param)
        progress.log(gen_cur + 1)
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
    progress.end()
    executor.exec_all()
    csv = CSV()
    csv.template("solver", "param", "time")
    for param, solver in product(inputs, solvers):
        results = executor.get_results(f"{param}{solver}")
        for secs in results:
            timeouts.new_result(solver, secs)
            csv.add_row(solver, param, secs)
        time_lists[solver][param] = mean(results)
    csv.save(name, export)
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
    decs = max(
        get_num_decimals(start),
        get_num_decimals(stop),
        get_num_decimals(step),
    )
    seq = []
    i = start
    while i < stop:
        n = round(i, decs)
        if n == round(stop, decs):
            break
        seq.append(n)
        i += step
    return seq


def get_num_decimals(num: float) -> int:
    parts = str(num).split(".")
    if len(parts) == 1:
        return 0
    return len(parts[1].rstrip("0"))
