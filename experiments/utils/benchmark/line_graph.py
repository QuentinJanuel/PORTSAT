from statistics import mean
from typing import List, Tuple, Callable
from utils.csv import CSV
from utils.graph import Graph
from utils.benchmark.benchmark import benchmark_solve
from utils.benchmark.randomized_executor import RandomizedExecutor, Job
from utils.benchmark.get_args import GetArgs
from utils.benchmark.timeouts import Timeouts
from utils.benchmark.export import Export
from utils.benchmark.inputs import Inputs
from utils.problem import Problem
from utils.progress import Progress
from itertools import product
from pathlib import Path
import matplotlib.pyplot as plt  # type: ignore


def bench(
    x_label: str,
    inputs: Inputs,
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
    inputs_seq = inputs.get(problem)
    timeouts = Timeouts(timeout)
    executor = RandomizedExecutor[Tuple[float, str | None]]()
    progress = Progress("Generation", len(inputs_seq) * repetitions)
    for gen_cur, (param, _) in enumerate(product(
        inputs_seq,
        range(repetitions),
    )):
        graph = graph_generator(param)
        progress.log(gen_cur + 1)
        get_args = GetArgs(graph, problem)
        for solver in solvers:
            for arg in get_args.get():
                def job_fun(
                    graph: Graph,
                    problem: Problem,
                    solver: str,
                    arg: str | None,
                    timeout: float,
                ) -> Tuple[float, str | None]:
                    secs = benchmark_solve(
                        graph=graph,
                        problem=problem,
                        solvers=[solver],
                        arg=arg,
                        timeout=timeout,
                    )
                    return secs, arg
                job = Job[Tuple[float, str | None]](
                    job_fun,
                    graph,
                    problem,
                    solver,
                    arg,
                    timeout,
                )
                executor.add(f"{param}{solver}", job)
    progress.end()
    executor.exec_all()
    csv = CSV()
    csv.template("solver", "param", "arg", "time")
    for param, solver in product(inputs_seq, solvers):
        results = executor.get_results(f"{param}{solver}")
        for secs, arg in results:
            timeouts.new_result(solver, secs)
            csv.add_row(solver, param, arg, secs)
        time_lists[solver][param] = mean([secs for secs, _ in results])
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
