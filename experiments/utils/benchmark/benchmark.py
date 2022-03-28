from time import time
from pathlib import Path
from typing import Callable, List, Any
from utils.solve import solve
from utils.problem import Problem
import re


def benchmark_fun(
    
    fun: Callable,
    *args: Any,
    **kwargs: Any,
) -> float:
    """
    Function takes a function and it's arguments and evaluate the time elapsed in the execution

    Parameters :
    ------------
    fun: Callable
    *args: Any
    **kwargs: Any

    Return :
    --------
    Execution time of the function : float
    """
    start = time()
    fun(*args, **kwargs)
    end = time()
    return end - start


def benchmark_solve(
    input: Path,
    problem: Problem,
    solvers: List[str],
    timeout: float,
    arg: str | None = None,
    mesure_only_sat_solving: bool = True,
) -> float:
    """
    Return benchmark of argumentation solver or just the sat solver:
    sat solver : Parse solver output 
    argumentation solver : python benchmarking (benchmark_fun)

    Parameters :
    ------------
    input: Path
    problem: Problem
    solvers: List[str]
    timeout: float
    arg: str | None = None
    mesure_only_sat_solving: bool = True

    Return :
    --------
    Execution time of the function : float
    """
    if mesure_only_sat_solving:
        output = solve(
            input=input,
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
            input=input,
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
