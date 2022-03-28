use crate::{
    af::{
        AF,
        Extension,
    },
    problem::Task,
};
use sat_portfolio::solver::{self as sat_solver, Solver};
use super::benchmark::BenchmarkTask;

pub fn solve(
    af: &AF,
    task: &Task,
    sat_solver: Option<Box<dyn Solver>>,
) -> Result<(), String> {
    if sat_solver.is_some() {
        return Err("You cannot choose the sat solver for the grounded extension.".into())
    }
    let cnf = benchmark!(
        BenchmarkTask::CNFGeneration,
        af.phi_co(),
    );
    let sat_solver = sat_solver::minisat::Minisat::new();
    let model = benchmark!(
        BenchmarkTask::SATSolving,
        sat_solver
            .solve(&cnf)
            .expect("The grounded extension should always exist")
    );
    let extension = Extension::new(&af, &model);
    match task {
        Task::FindOne => println!("{}", extension),
        Task::Enumerate => println!("[{}]", extension),
        Task::Credulous(arg) | Task::Skeptical(arg) => {
            if extension.contains(arg) {
                println!("YES");
            } else {
                println!("NO");
            }
        },
    };
    Ok(())
}