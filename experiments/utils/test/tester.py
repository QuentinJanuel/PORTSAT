from pathlib import Path
from typing import List
from utils.test.ext_parser import parse_extension, parse_extensions
from utils.solve import solve


def test(
    testers: List["Tester"],
    solvers: List[str],
    semantics: List[str],
    tasks: List[str],
) -> bool:
    for i, tester in enumerate(testers):
        print(f"Tester {i + 1}/{len(testers)}")
        if not tester.test(solvers, semantics, tasks):
            return False
    return True


class Tester:
    def __init__(self, input: Path):
        self._input = input

    def get_input(self) -> Path:
        return self._input

    def get_solution(self, sem: str) -> str:
        solution = ""
        file = self._get_solution_file(sem)
        with open(file, "r") as f:
            for line in f:
                solution += line
        return solution

    def test(
        self,
        solvers: List[str],
        semantics: List[str],
        tasks: List[str],
    ) -> bool:
        for task in tasks:
            for sem in semantics:
                for solver in solvers:
                    guess = solve(
                        input=self.get_input(),
                        problem=f"{task}-{sem}",
                        solvers=[solver],
                        format="tgf",
                        arg=None,
                    )
                    if not self.check(guess, task, sem):
                        print("Wrong answer")
                        print(f"Problem: {task}-{sem}")
                        print(f"Solver: {solver}")
                        print(f"Input: {self.get_input()}")
                        print("All extensions: {}".format(
                            self._get_solution_file(sem)
                        ))
                        print(f"Guess: {guess}")
                        return False
        return True

    def check(self, guess: str, task: str, sem: str):
        r_exts = parse_extensions(self.get_solution(sem))
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
            for ext2 in exts2:
                if not self._comp_ext(ext1, ext2):
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
