from pathlib import Path
from typing import List, Literal, Tuple
from utils.test.ext_parser import parse_extension, parse_extensions
from utils.solve import solve
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt

class Tester:
    def __init__(self, input: Path, type: Literal["gr", "st", "scc"]):
        self._input = input
        self._type = type

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
        progress: Tuple[int, int],
        timeout_count: int,
        timeout: float | None = None,
    ) -> Tuple[bool, int,pd.DataFrame]:
        df=pd.DataFrame(columns=["TaskSem"]+solvers)
        for task in tasks:
            for sem in semantics:
                row={"TaskSem":f"{task}-{sem}"}
                for solver in solvers:
                    print(
                        " ".join([
                            "\r",
                            f"Tester {progress[0]}/{progress[1]}",
                            self._type,
                            f"{task}-{sem}",
                            solver if solver is not None else "default",
                            f"Timeouts: {timeout_count}",
                            " " * 20,
                        ]),
                        end="",
                    )
                    startTimer=time.time()
                    guess = solve(
                        input=self.get_input(),
                        problem=f"{task}-{sem}",
                        solvers=[solver] if solver is not None else None,
                        format="tgf",
                        arg=None,
                        timeout=timeout,
                    )
                    endTimer=time.time()
                    row.update({solver:endTimer-startTimer})
                    if guess is None:
                        timeout_count += 1
                        continue
                    if not self.check(guess, task, sem):
                        print("Wrong answer")
                        print(f"Problem: {task}-{sem}")
                        print(f"Solver: {solver}")
                        print(f"Input: {self.get_input()}")
                        print("All extensions: {}".format(
                            self._get_solution_file(sem)
                        ))
                        print(f"Guess: {guess}")
                        df=pd.concat([df,pd.DataFrame([row],columns=row.keys())],ignore_index=True)
                        return False, timeout_count,df
                    
                df=pd.concat([df,pd.DataFrame([row],columns=row.keys())],ignore_index=True)

        return (True, timeout_count,df)

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
    def __str__(self):
        return str(self._input.name)
def test(
    testers: List["Tester"],
    solvers: List[str],
    semantics: List[str],
    tasks: List[str],
    timeout: float | None = None,
) -> bool:
    timeout_count = 0
    finalCsv=pd.DataFrame()
    for i, tester in enumerate(testers):
        success, timeout_count,df= tester.test(
            solvers,
            semantics,
            tasks,
            progress=(i + 1, len(testers)),
            timeout_count=timeout_count,
            timeout=timeout,
        )
        df["testFileName"]=str(tester)
        if not success:
            print()
            print("FAILED")
            return False
        finalCsv=pd.concat([finalCsv,df])
    finalCsv.fillna(-2,inplace=True)
    finalCsv.to_csv("TEST1234.csv",index=False)
    return True

def displayGraph(csv):
    df=pd.read_csv(csv)
    color=["blue","red","orange","green"]
    width=0.35

    solvers=list(df.columns)[1:-1]
    dfTransformed=df.groupby(["TaskSem"]).mean()
    x=list(set(df["TaskSem"]))
    ind=np.arange(len(x))
    pas=width/len(solvers)
    for i,solver in enumerate(solvers):
        bench=list(dfTransformed[solver])
        j=2
        if(i>len(solvers)/2):
            
            plt.bar(ind-(pas)*(j-1),bench,width=pas,label=solver,color=color[i])
            j+=1
        elif(len(solvers)==2 and i==2):
            plt.bar(ind-(pas)*(1),bench,width=pas,label=solver,color=color[i])
        else:
            plt.bar(ind+(pas)*(i),bench,width=pas,label=solver,color=color[i])
    plt.xticks(ind,x)
    plt.legend(loc="upper right")
    plt.show()