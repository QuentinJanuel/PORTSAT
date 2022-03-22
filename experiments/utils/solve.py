import os
import subprocess
from pathlib import Path
from typing import List
from utils.problem import Problem
from utils.iccma.type import Format


def get_exe():
    return Path().joinpath(
        os.getcwd(),
        "..",
        "target",
        "release",
        "ter",
    ).resolve()


def solve(
    input: Path,
    problem: Problem,
    arg: str | None = None,
    solvers: List[str] | None = None,
    format: Format = "tgf",
    timeout: float | None = None,
    opt_flags: List[str] = [],
) -> str | None:
    try:
        result = subprocess.run(
            [
                get_exe(),
                "-p",
                str(problem),
                "-f",
                input,
                "-fo",
                format,
                *([] if arg is None else ["-a", arg]),
                *([] if solvers is None else ["-s", ",".join(solvers)]),
                *opt_flags,
            ],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode != 0:
            raise Exception(result.stderr)
        return result.stdout
    except subprocess.TimeoutExpired:
        return None
