from typing import List
from utils.iccma.iccma_graph import ICCMAGraph
from utils.benchmark.benchmark import benchmark_solve
from utils.problem import Task, Semantics, Problem
import numpy as np
import pandas as pd  # type: ignore
import matplotlib.pyplot as plt  # type: ignore


def bench(
    graphs: List["ICCMAGraph"],
    solvers: List[str],
    semantics: List[Semantics],
    tasks: List[Task],
    timeout: float,
):
    final_csv = pd.DataFrame()
    for graph in graphs:
        df = pd.DataFrame(columns=["problem"]+solvers)
        for task in tasks:
            for sem in semantics:
                problem = Problem(task, sem)
                row = {"problem": str(problem)}
                for solver in solvers:
                    secs = benchmark_solve(
                        input=graph.get_input(),
                        problem=problem,
                        solvers=[solver],
                        arg=None,
                        timeout=timeout,
                    )
                    row.update({solver: str(secs)})
                df = pd.concat(
                    [
                        df,
                        pd.DataFrame([row], columns=row.keys()),
                    ],
                    ignore_index=True,
                )
        df["testFileName"] = graph.get_input().name
        final_csv = pd.concat([final_csv, df])
    final_csv.fillna(-2, inplace=True)
    final_csv.to_csv("TEST1234.csv", index=False)


def display_graph(csv):
    df = pd.read_csv(csv)
    color = ["blue", "red", "orange", "green"]
    width = 0.35
    solvers = list(df.columns)[1:-1]
    df_transformed = df.groupby(["problem"]).mean()
    x = list(set(df["problem"]))
    ind = np.arange(len(x))
    pas = width/len(solvers)
    for i, solver in enumerate(solvers):
        bench = list(df_transformed[solver])
        j = 2
        if i > len(solvers) / 2:
            plt.bar(
                ind - pas * (j - 1),
                bench,
                width=pas,
                label=solver,
                color=color[i],
            )
            j += 1
        elif len(solvers) == 2 and i == 2:
            plt.bar(
                ind - pas,
                bench,
                width=pas,
                label=solver,
                color=color[i],
            )
        else:
            plt.bar(
                ind + pas * i,
                bench,
                width=pas,
                label=solver,
                color=color[i],
            )
    plt.xticks(ind, x)
    plt.legend(loc="upper right")
    plt.show()
