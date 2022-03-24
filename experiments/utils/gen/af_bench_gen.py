import os
import subprocess
from pathlib import Path
from typing import Literal
from utils.graph import Graph


def get_jar():
    return Path().joinpath(
        os.getcwd(),
        "utils",
        "gen",
        "AFBenchGen.jar"
    ).resolve()


Type = Literal["BarabasiAlbert", "WattsStrogatz", "ErdosRenyi"]


def generate_graph(
    num_args: int,
    type: Type,
    ba_ws_prob_cycles: float = 0.0,
    er_prob_attacks: float = 0.0,
    ws_base_degree: int = 0,
    ws_beta: float = 0.0,
) -> Graph:
    result = subprocess.run(
        [
            "java",
            "-jar",
            get_jar(),
            "-numargs",
            str(num_args),
            "-type",
            type,
            "-BA_WS_probCycles",
            str(ba_ws_prob_cycles),
            "-ER_probAttacks",
            str(er_prob_attacks),
            "-WS_baseDegree",
            str(ws_base_degree),
            "-WS_beta",
            str(ws_beta)
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise Exception(result.stderr)
    return Graph.from_apx(result.stdout)
