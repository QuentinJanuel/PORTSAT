import os
import tempfile
import shutil
import subprocess
from pathlib import Path
from typing import List, TYPE_CHECKING
from utils.problem import Problem
from utils.iccma.type import Format

if TYPE_CHECKING:
    from utils.graph import Graph


def get_exe():
    return Path().joinpath(
        os.getcwd(),
        "..",
        "target",
        "release",
        "ter",
    ).resolve()


def solve(
    graph: "Graph",
    problem: Problem,
    arg: str | None = None,
    solvers: List[str] | None = None,
    format: Format = "tgf",
    timeout: float | None = None,
    opt_flags: List[str] = [],
) -> str | None:
    tmp: Path | None = None
    try:
        tmp = Path(tempfile.mkdtemp())
        file: Path | None = None
        if format == "tgf":
            file = graph.save_tgf(tmp.joinpath("tmp_graph.tgf"))
        elif format == "apx":
            file = graph.save_apx(tmp.joinpath("tmp_graph.apx"))
        else:
            raise ValueError(f"Unknown format: {format}")
        result = subprocess.run(
            [
                get_exe(),
                "-p",
                str(problem),
                "-f",
                file,
                "-fo",
                format,
                *([] if arg is None else ["-a", str(arg)]),
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
    finally:
        if tmp is not None:
            shutil.rmtree(tmp)
