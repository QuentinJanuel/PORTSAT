use std::fmt;

pub enum BenchmarkTask {
    CNFGeneration,
    SATSolving,
}

impl fmt::Display for BenchmarkTask {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            BenchmarkTask::CNFGeneration => write!(f, "CNF generation"),
            BenchmarkTask::SATSolving => write!(f, "SAT solving"),
        }
    }
}
