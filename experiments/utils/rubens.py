import subprocess
import matplotlib.pyplot as plt
import numpy as np
from solve import solve
from typing import List


rubens_jar = "/home/christophe/programs/rubens/rubens-fr.cril.rubens.pom-1.1.2/fr.cril.rubens.checker/target/rubens-checker-1.1.2.jar"


def rubens_checker(problem: str, output_dir: str, rubens_jar_path: str):
    result = subprocess.run(
        [
            "java",
            "-jar",
            rubens_jar_path,
            "-m",
            problem,
            "-o",
            output_dir,
            "-e",
            solve.get_exe(),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise Exception(result.stderr)
    return result.stdout


# semantics : [GR,ST,CO,PR]
def benchmark(input: str, solvers: List[str], semantics: List[str]):
    _, ax = plt.subplots(1, 1)
    problems = ["EE", "SE", "DS", "DC"]
    argument = str(1)
    data = [["" for _ in range(len(semantics)*len(problems))]
            for _ in range(len(solvers))]
    column_labels = []
    for i_sol, solver in enumerate(solvers):
        for i_sem, semantic in enumerate(semantics):
            for i_pro, problem in enumerate(problems):
                # arg = None
                # if(problem[0] == "D"):
                #     arg = argument
                column_labels.append(problem + "-" + semantic)
                data[i_sol][i_sem + i_pro] = solve(
                    input,
                    problem + "-" + semantic,
                    solvers=[solver],
                    arg=argument,
                )[1]
    rowLabels = solvers
    ax.axis("tight")
    ax.axis("off")
    ax.table(
        cellText=data,
        colLabels=column_labels,
        rowLabels=rowLabels,
        loc="center",
    )
    plt.show()


def checkEquality(problem: str, arrayToTest, solutions: str = ""):
    with open(solutions, "r") as solution:
        solutionArray = np.array(json.loads(
            solution.read().strip().replace("a", "")), dtype=object)
    arr = np.array(json.loads(
        arrayToTest.strip().replace("a", "")), dtype=object)
    if(problem == "SE"):
        for i in range(len(arr)):
            for j in range(len(solutionArray)):
                if(set(arr[i]) == set(solutionArray[j])):
                    return True
        return False
    elif(problem == "EE"):
        testAll = [False for _ in range(len(solutionArray))]
        for i in range(len(arr)):
            for j in range(len(solutionArray)):
                if(set(arr[i]) == set(solutionArray[j])):
                    testAll[j] = True
        for test in testAll:
            if(not(test)):
                return False
        return True
    else:
        print("Probleme non traité")
        return False
