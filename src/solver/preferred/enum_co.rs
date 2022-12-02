use crate::{
    af::{
        AF,
        Extension,
    },
    problem::Task,
};
use sat_portfolio::solver::Solver;
use super::super::benchmark::BenchmarkTask;

pub fn solve(
    af: &AF,
    task: &Task,
    sat_solver: Option<Box<dyn Solver>>,
) {
    let sat_solver = sat_solver
        .unwrap_or_else(|| Box::new(sat_portfolio::solver::manysat::Manysat::new()));
    let mut cnf = benchmark!(
        BenchmarkTask::CNFGeneration,
        af.phi_co(),
    );
    let models = benchmark!(
        BenchmarkTask::SATSolving,
        sat_solver
            .get_all_models(&mut cnf),
    );
    if let Task::FindOne = task {
        let model = models
            .iter()
            .reduce(|a, b| {
                let a_len = a.get_pos_vars().len();
                let b_len = b.get_pos_vars().len();
                if a_len >= b_len { a } else { b }
            })
            .expect("There should always exist at least one preferred extension");
        println!("{}", Extension::new(&af, &model));
    } else {
        let extensions = models.iter()
            .map(|m| Extension::new(&af, &m))
            .collect::<Vec<_>>();
        let mut preferred = vec![];
        for (i, ext) in extensions
            .iter()
            .enumerate()
        {
            let is_preferred = extensions
                .iter()
                .enumerate()
                .all(|(j, other)| {
                    i == j || !ext.is_subset(&other)
                });
            if is_preferred {
                preferred.push(ext);
            }
        }
        match task {
            Task::Enumerate => println!("[{}]", preferred.iter()
                .map(|e| e.to_string())
                .collect::<Vec<_>>()
                .join(", "),
            ),
            Task::Credulous(arg) => {
                let extension = preferred
                    .iter()
                    .find(|e| e.contains(arg));
                if let Some(extension) = extension {
                    println!("YES");
                    println!("{}", extension);
                } else {
                    println!("NO");
                }
            },
            Task::Skeptical(arg) => {
                let extension = preferred
                    .iter()
                    .find(|e| !e.contains(arg));
                if let Some(extension) = extension {
                    println!("NO");
                    println!("{}", extension);
                } else {
                    println!("YES");
                }
            },
            _ => unreachable!(),
        }
    }
}
