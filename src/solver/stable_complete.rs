use crate::{
    af::{
        AF,
        Extension,
    },
    problem::Task,
};
use sat_portfolio::{
    cnf::{
        Clause,
        Lit,
        CNF,
    },
    solver::Solver,
};
use super::benchmark::BenchmarkTask;

pub fn solve<F>(
    af: &AF,
    gen_cnf: F,
    task: &Task,
    sat_solver: Option<Box<dyn Solver>>,
)
where
    F: FnOnce() -> CNF,
{
    let sat_solver = sat_solver
        .unwrap_or_else(|| Box::new(sat_portfolio::solver::manysat::Manysat::new()));
    let cnf = benchmark!(
        BenchmarkTask::CNFGeneration,
        gen_cnf(),
    );
    match task {
        Task::FindOne => {
            let model = benchmark!(
                BenchmarkTask::SATSolving,
                sat_solver.solve(&cnf),
            );
            if let Some(model) = model {
                println!("{}", Extension::new(af, &model));
            } else {
                println!("NO");
            }
        },
        Task::Enumerate => {
            let mut cnf = cnf;
            let models = benchmark!(
                BenchmarkTask::SATSolving,
                sat_solver
                    .get_all_models(&mut cnf),
            );
            println!("[{}]", models
                .iter()
                .map(|m| format!("{}", Extension::new(af, m)))
                .collect::<Vec<_>>()
                .join(","),
            )
        }
        Task::Credulous(arg) => {
            let mut cnf = cnf;
            cnf.add_clause(Clause::from(vec![
                Lit::pos(af.get_var(arg))
            ]));
            let model = benchmark!(
                BenchmarkTask::SATSolving,
                sat_solver.solve(&cnf),
            );
            if let Some(_) = model {
                println!("YES");
            } else {
                println!("NO");
            }
        },
        Task::Skeptical(arg) => {
            let mut cnf = cnf;
            cnf.add_clause(Clause::from(vec![
                Lit::neg(af.get_var(arg))
            ]));
            let model = benchmark!(
                BenchmarkTask::SATSolving,
                sat_solver.solve(&cnf),
            );
            if let Some(_) = model {
                println!("NO");
            } else {
                println!("YES");
            }
        },
    }
}