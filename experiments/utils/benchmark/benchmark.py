from time import time
from pathlib import Path
from typing import List
from utils.solve import solve
from utils.problem import Problem
import re


def benchmark_fun(fun, *args, **kwargs) -> float:
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
