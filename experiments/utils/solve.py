import os
import subprocess
from pathlib import Path
from typing import List


def get_exe():
    return Path().joinpath(
        os.getcwd(),
        "..",
        "target",
        "release",
        "ter",
    ).resolve()


def solve(
    input: str,
    problem: str,
    arg: str = None,
    solvers: List[str] = None,
):
    result = subprocess.run(
        [
            get_exe(),
            "-p",
            problem,
            "-f",
            f"graph/{input}",
            *([] if arg is None else ["-a", arg]),
            *([] if solvers is None else ["-s", ",".join(solvers)]),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise Exception(result.stderr)
    return result.stdout