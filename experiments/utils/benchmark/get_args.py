from typing import List
from utils.graph import Graph
from utils.problem import Task, Problem


class GetArgs:
    def __init__(
        self,
        graph: Graph,
        problem: Problem,
        timeout: float | None = None,
    ):
        self._vertices: List[str] = graph.vertices
        self._problem: Problem = problem
        self._extensions: List[List[str]] | None = graph.get_extensions(
            self._problem.get_sem(),
            timeout,
        )
        self._cred: str | None = None
        self._non_cred: str | None = None
        self._skept: str | None = None
        self._non_skept: str | None = None
        self._gen()

    def _gen(self):
        if self._extensions is None:
            return
        if len(self._vertices) == 0:
            return
        if len(self._extensions) == 0:
            self._cred = self._vertices[0]
            self._non_cred = self._vertices[0]
            self._skept = self._vertices[0]
            self._non_skept = self._vertices[0]
        else:
            some_ext = self._extensions[0]
            all_exts = set(some_ext)
            for ext in self._extensions[1:]:
                all_exts = all_exts.intersection(set(ext))
            all_exts = list(all_exts)
            not_some_ext = list(set(self._vertices) - set(some_ext))
            not_all_exts = list(set(self._vertices) - set(all_exts))
            if len(some_ext) > 0:
                self._cred = some_ext[0]
            if len(all_exts) > 0:
                self._skept = some_ext[0]
            if len(not_some_ext) > 0:
                self._non_cred = not_some_ext[0]
            if len(not_all_exts) > 0:
                self._non_skept = not_all_exts[0]

    def get(self) -> List[str | None]:
        args: List[str | None] = []
        task: Task = self._problem.get_task()
        if task == "DC":
            if self._cred is not None:
                args.append(self._cred)
            if self._non_cred is not None:
                args.append(self._non_cred)
        elif task == "DS":
            if self._skept is not None:
                args.append(self._skept)
            if self._non_skept is not None:
                args.append(self._non_skept)
        else:
            args.append(None)
        return args
