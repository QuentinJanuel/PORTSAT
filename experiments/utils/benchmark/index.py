from statistics import mean
from typing import Dict, List
from utils.iccma.iccma_graph import ICCMAGraph
from utils.benchmark.benchmark import benchmark_solve
from utils.problem import Task, Semantics, Problem
import numpy as np
import matplotlib.pyplot as plt  # type: ignore
from itertools import product
from math import floor


def bench(
    graphs: List["ICCMAGraph"],
    solvers: List[str],
    semantics: List[Semantics],
    tasks: List[Task],
    timeout: float,
):
    stats: Dict[str, float] = {}
    problems: List[Problem] = [
        Problem(task, sem)
        for task, sem in product(tasks, semantics)
    ]
    cur_progress = 0
    max_progress = len(solvers) * len(problems) * len(graphs)
    for solver, problem in product(solvers, problems):
        all_secs: List[float] = []
        for graph in graphs:
            secs = benchmark_solve(
                input=graph.get_input(),
                problem=problem,
                solvers=[solver],
                arg=None,
                timeout=timeout,
            )
            all_secs.append(secs)
            cur_progress += 1
            percent = cur_progress / max_progress * 100
            print(f"\r{floor(percent)}%" + 10 * " ", end="")
        secs = mean(all_secs)
        stats[f"{solver}{problem}"] = secs
    labels = [str(p) for p in problems]
    x = np.arange(len(labels))
    width = 1 / (len(solvers) + 1)
    total_width = width * len(solvers)
    _, ax = plt.subplots()
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
    ax.set_title(get_title(graphs))
    ax.set_ylabel("Time (s)")
    ax.set_xticks(x, labels)
    ax.legend()
    plt.show()


def get_title(graphs: List["ICCMAGraph"]) -> str:
    categories = [f"{g.get_type()}-{g.get_size()}" for g in graphs]
    return ", ".join([*{*categories}])
