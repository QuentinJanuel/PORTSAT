from time import time
from typing import Callable, List, Any
from utils.solve import solve
from utils.problem import Problem
from utils.graph import Graph
import re


def benchmark_fun(
    fun: Callable,
    *args: Any,
    **kwargs: Any,
) -> float:
    """
    Runs the function passed as parameter
    and returns the execution time in seconds.

    Example :
    ---------
    >>> def sum(a, b):
    ...     return a + b
    ...
    >>> benchmark_fun(sum, 1, 2)
    """
    start = time()
    fun(*args, **kwargs)
    end = time()
    return end - start


def benchmark_solve(
    graph: Graph,
    problem: Problem,
    solvers: List[str],
    timeout: float,
    arg: str | None = None,
    mesure_only_sat_solving: bool = True,
) -> float:
    """
    Returns the execution time in seconds of
    the solver and problem passed as parameters.

    Parameters :
    ------------
    input: the path to the input file
    problem: the problem to solve
    solvers: the list of solvers to use, they will be executed in parallel
    timeout: (seconds) if the solver times out,
    it will return 10 times the timeout
    arg: (optional) the argument to check for DS and DC tasks
    mesure_only_sat_solving: (default is True) if set to true,
    only the SAT part will be measured

    Example :
    ---------
    >>> benchmark_solve(
    ...     Path("input.tgf"),
    ...     Problem("SE", "GR"),
    ...     ["minisat"],
    ...     10 * 60,
    ... )
    """
    if mesure_only_sat_solving:
        output = solve(
            graph=graph,
            problem=problem,
            arg=arg,
            solvers=solvers,
            format="tgf",
            timeout=timeout,
            opt_flags=["-v"],
        )
        if output is None:
            return timeout * 10
        ms_str = re.search(
            r"SAT solving done in (\d+)ms",
            output,
            re.MULTILINE,
        )
        if ms_str is None:
            raise Exception("Failed to parse the SAT solving time")
        ms = int(ms_str.groups()[0])
        s = ms / 1000
        if s > timeout:
            return timeout * 10
        return s
    else:
        s = benchmark_fun(
            solve,
            graph=graph,
            problem=problem,
            arg=arg,
            solvers=solvers,
            format="tgf",
            timeout=timeout,
            opt_flags=["-v"],
        )
        if s > timeout:
            return timeout * 10
        return s
