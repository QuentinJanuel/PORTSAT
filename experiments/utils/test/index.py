from typing import List
from utils.iccma.type import Format
from utils.iccma.iccma_graph import ICCMAGraph
from utils.solve import solve
from itertools import product
from math import floor
from utils.problem import Semantics, Task, Problem


def test(
    graphs: List["ICCMAGraph"],
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
        graphs,
        tasks,
        semantics,
        maybe_solvers,
    )
    prod_len = len(graphs) * len(tasks) * len(semantics) * len(maybe_solvers)
    for graph, task, sem, solver in prod:
        progress = floor(100 * (total_count + 1) / prod_len)
        problem = Problem(task, sem)
        print(
            " ".join([
                "\r",
                f"{progress}%",
                graph.get_type(),
                str(problem),
                solver if solver is not None else "default",
                f"Timeouts: {timeout_count}/{total_count}",
                " " * 20,
            ]),
            end="",
        )
        guess = solve(
            input=graph.get_input(format),
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
        if not graph.check(guess, problem):
            print("Wrong answer")
            print(f"Problem: {problem}")
            print(f"Solver: {solver}")
            print(f"Input: {graph.get_input()}")
            print("All extensions: {}".format(
                graph._get_solution_file(sem)
            ))
            print(f"Guess: {guess}")
            print()
            print("FAILED")
            return False
    print()
    print("OK")
    return True
