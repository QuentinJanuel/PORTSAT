from typing import Literal


Task = Literal["SE", "EE", "DC", "DS"]
Semantics = Literal["GR", "CO", "PR", "ST"]


class Problem:
    def __init__(self, task: Task, sem: Semantics):
        self._task: Task = task
        self._sem: Semantics = sem

    def get_task(self) -> Task:
        return self._task

    def get_sem(self) -> Semantics:
        return self._sem

    def __str__(self):
        return f"{self._task}-{self._sem}"
