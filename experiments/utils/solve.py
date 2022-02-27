import os
import subprocess
from pathlib import Path
from typing import List, Literal


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
    problem: str,
    arg: str | None = None,
    solvers: List[str] | None = None,
    format: Literal["tgf", "apx"] = "tgf",
    timeout: float | None = None,
) -> str | None:
    try:
        result = subprocess.run(
            [
                get_exe(),
                "-p",
                problem,
                "-f",
                input,
                "-fo",
                format,
                *([] if arg is None else ["-a", arg]),
                *([] if solvers is None else ["-s", ",".join(solvers)]),
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
