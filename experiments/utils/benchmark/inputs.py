from typing import Sequence, Tuple
from utils.problem import Task, Semantics, Problem


class Inputs:
    def __init__(self, default: Sequence[float] | None = None):
        self._default = default
        self._cases: dict[
            Tuple[
                Task | None,
                Semantics | None,
            ],
            Sequence[float],
        ] = {}

    def task(self, task: Task, inputs: Sequence[float]) -> "Inputs":
        self._cases[(task, None)] = inputs
        return self

    def sem(self, sem: Semantics, inputs: Sequence[float]) -> "Inputs":
        self._cases[(None, sem)] = inputs
        return self

    def prob(
        self,
        task: Task,
        sem: Semantics,
        inputs: Sequence[float],
    ) -> "Inputs":
        self._cases[(task, sem)] = inputs
        return self

    def get(self, problem: Problem) -> Sequence[float]:
        task = problem.get_task()
        sem = problem.get_sem()
        inputs = self._default
        precision = 0
        for (c_task, c_sem), c_inputs in self._cases.items():
            task_matches = c_task is None or task == c_task
            sem_matches = c_sem is None or sem == c_sem
            c_precision = 0
            if c_task is not None:
                c_precision += 1
            if c_sem is not None:
                c_precision += 1
            if task_matches and sem_matches and c_precision >= precision:
                inputs = c_inputs
                precision = c_precision
        if inputs is None:
            raise Exception("No default inputs")
        return inputs


def frange(start: float, stop: float, step: float) -> Sequence[float]:
    decs = max(
        get_num_decimals(start),
        get_num_decimals(stop),
        get_num_decimals(step),
    )
    seq = []
    i = start
    while i < stop:
        n = round(i, decs)
        if n == round(stop, decs):
            break
        seq.append(n)
        i += step
    return seq


def get_num_decimals(num: float) -> int:
    parts = str(num).split(".")
    if len(parts) == 1:
        return 0
    return len(parts[1].rstrip("0"))
