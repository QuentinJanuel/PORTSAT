from pathlib import Path
from typing import List
from utils.iccma.ext_parser import parse_extension, parse_extensions
from utils.iccma.type import GraphType, Format, Size
from utils.problem import Problem


class ICCMAGraph:
    def __init__(self, input: Path, type: GraphType, size: Size):
        self._input = input
        self._type: GraphType = type
        self._size: Size = size

    def get_input(self, format: Format = "tgf") -> Path:
        if format == "tgf":
            return self._input
        return self\
            ._input\
            .parent\
            .joinpath(f"{self._input.stem}.apx")

    def get_type(self) -> GraphType:
        return self._type

    def get_size(self) -> Size:
        return self._size

    def get_solution(self, sem: str) -> str:
        solution = ""
        file = self._get_solution_file(sem)
        with open(file, "r") as f:
            for line in f:
                solution += line
        return solution

    def check(self, guess: str, problem: Problem):
        r_exts = parse_extensions(self.get_solution(problem.get_sem()))
        task = problem.get_task()
        if task == "SE":
            g_ext = parse_extension(guess)
            if g_ext is None:
                return len(r_exts) == 0
            for r_ext in r_exts:
                if self._comp_ext(g_ext, r_ext):
                    return True
            return False
        elif task == "EE":
            g_exts = parse_extensions(guess)
            return self._comp_exts(g_exts, r_exts)
        elif task == "DS":
            pass
        elif task == "DC":
            pass
        else:
            raise Exception(f"Unknown task: {task}")

    def _get_solution_file(
        self,
        sem: str,
    ) -> Path:
        solution = self._input\
            .parent\
            .joinpath(
                f"{self._input.stem}.apx.EE-{sem}",
            )
        assert solution.exists()
        return solution

    def _comp_ext(
        self,
        ext1: List[str],
        ext2: List[str],
    ) -> bool:
        if len(ext1) != len(ext2):
            return False
        return sorted(ext1) == sorted(ext2)

    def _exts_inclusion(
        self,
        exts1: List[List[str]],
        exts2: List[List[str]],
    ) -> bool:
        for ext1 in exts1:
            is_in = False
            for ext2 in exts2:
                if self._comp_ext(ext1, ext2):
                    is_in = True
                    break
            if not is_in:
                return False
        return True

    def _comp_exts(
        self,
        exts1: List[List[str]],
        exts2: List[List[str]],
    ) -> bool:
        if len(exts1) != len(exts2):
            return False
        a = self._exts_inclusion(exts1, exts2)
        b = self._exts_inclusion(exts2, exts1)
        return a and b
