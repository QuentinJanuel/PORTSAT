from typing import List
from utils.iccma.type import Format
from utils.iccma.iccma_graph import ICCMAGraph
from utils.solve import solve
from utils.graph import Graph
from itertools import product
from math import floor
from utils.problem import Semantics, Task, Problem


def test(
    iccma_graphs: List["ICCMAGraph"],
    solvers: List[str],
    semantics: List[Semantics],
    tasks: List[Task],
    timeout: float | None = None,
    format: Format = "tgf",
) -> bool:
    timeout_count, total_count = 0, 0
    maybe_solvers: List[str | None] = [solver for solver in solvers]
    if len(maybe_solvers) == 0:
        maybe_solvers.append(None)
    prod = product(
        iccma_graphs,
        tasks,
        semantics,
        maybe_solvers,
    )
    prod_len = 1
    prod_len *= len(iccma_graphs)
    prod_len *= len(tasks)
    prod_len *= len(semantics)
    prod_len *= len(maybe_solvers)
    for iccma_graph, task, sem, solver in prod:
        progress = floor(100 * (total_count + 1) / prod_len)
        problem = Problem(task, sem)
        print(
            " ".join([
                "\r",
                f"{progress}%",
                iccma_graph.get_type(),
                str(problem),
                solver if solver is not None else "default",
                f"Timeouts: {timeout_count}/{total_count}",
                " " * 20,
            ]),
            end="",
        )
        graph = Graph.from_iccma_graph(iccma_graph)
        guess = solve(
            graph=graph,
            problem=problem,
            solvers=[solver] if solver is not None else None,
            format=format,
            arg=None,
            timeout=timeout,
        )
        total_count += 1
        if guess is None:
            timeout_count += 1
            continue
        if not iccma_graph.check(guess, problem):
            print("Wrong answer")
            print(f"Problem: {problem}")
            print(f"Solver: {solver}")
            print(f"Input: {iccma_graph.get_input()}")
            print("All extensions: {}".format(
                iccma_graph._get_solution_file(sem)
            ))
            print(f"Guess: {guess}")
            print()
            print("FAILED")
            return False
    print()
    print("OK")
    return True
