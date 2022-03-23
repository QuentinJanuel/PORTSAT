import os
import subprocess
from pathlib import Path

def get_jar():
    return Path().joinpath(
        "java -jar ",
        os.getcwd(),
        "utils",
        "gen",
        "AFBenchGen.jar"
    ).resolve()

"""
usage: jAFBenchGen
 -BA_WS_probCycles <floating point number>         probability that an
                                                   argument is part of a
                                                   cycle (used with
                                                   BarabasiAlbert and
                                                   WattsStrogatz only)
 -display                                          display the generated
                                                   graph
 -ER_probAttacks <floating point number>           probability of having
                                                   an attack between two
                                                   arguments (used with
                                                   ErdosRenyi only)
 -help                                             print this message
 -numargs <positive integer>                       number of arguments
 -type <BarabasiAlbert|WattsStrogatz|ErdosRenyi>   structure type
 -version                                          display version
 -WS_baseDegree <positive integer>                 base degree for each
                                                   node (used with
                                                   WattsStrogatz only). It
                                                   must be the case that
                                                   nunmargs >> baseDegree
                                                   >> log(baseDegree) >> 1
                                                   to guarantee that the
                                                   graph is connected.
 -WS_beta <floating point number>                  probability to 'rewire'
                                                   an edge (used with
                                                   ErdosRenyi only)

"""
def generateGraph(
    numargs : int,
    typeGraph : str,
    BA_WS_probCycles = 0.0,#FLOAT
    ER_probAttacks=0.0,#FLOAT
    WS_baseDegree = 0 ,#INT
    WS_beta = 0.0,#FLOAT
    grapheName=""
):
    typeList=["BarabasiAlbert","WattsStrogatz","ErdosRenyi"]
    if(typeGraph not in typeList):
        return None
    try:
        result = subprocess.run(
            [
                "java",
                "-jar",
                get_jar(),
                "-numargs",
                str(numargs),
                "-type",
                str(typeGraph),
                "-BA_WS_probCycles",
                str(BA_WS_probCycles),
                "-ER_probAttacks",
                str(ER_probAttacks),
                "-WS_baseDegree",
                str(WS_baseDegree),
                "-WS_beta",
                str(WS_beta)
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise Exception(result.stderr)
        if(grapheName!=""):
            with open(grapheName+".apx","w") as exportFile:
                exportFile.write(result.stdout)
        return result.stdout
    except subprocess.TimeoutExpired:
        return None
