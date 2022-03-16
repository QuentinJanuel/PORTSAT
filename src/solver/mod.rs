mod benchmark;

use crate::{
    af::{
        AF,
        Extension,
    },
    problem::{
        Problem,
        Semantics::*,
        Task::*,
    },
};
use sat_portfolio::{
    cnf::{
        Clause,
        Lit,
    },
    solver::{self as sat_solver, Solver},
};
use benchmark::BenchmarkTask;

pub fn solve(
    af: AF,
    problem: Problem,
    sat_solver: Option<Box<dyn Solver>>,
) -> Result<(), String> {
    match &problem.semantics {
        Complete | Stable => {
            let sat_solver = sat_solver
                .unwrap_or_else(|| Box::new(sat_portfolio::solver::manysat::Manysat::new()));
            let cnf = benchmark!(
                BenchmarkTask::CNFGeneration,
                if let Complete = &problem.semantics {
                    af.phi_co()
                } else {
                    af.phi_st()
                },
            );
            match &problem.task {
                FindOne => {
                    let model = benchmark!(
                        BenchmarkTask::SATSolving,
                        sat_solver.solve(&cnf),
                    );
                    if let Some(model) = model {
                        println!("{}", Extension::new(&af, &model));
                    } else {
                        println!("NO");
                    }
                },
                Enumerate => {
                    let mut cnf = cnf;
                    let models = benchmark!(
                        BenchmarkTask::SATSolving,
                        sat_solver
                            .get_all_models(&mut cnf),
                    );
                    println!("[{}]", models
                        .iter()
                        .map(|m| format!("{}", Extension::new(&af, m)))
                        .collect::<Vec<_>>()
                        .join(","),
                    )
                }
                Credulous(arg) => {
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
                Skeptical(arg) => {
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
        },
        Grounded => {
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
            match &problem.task {
                FindOne => println!("{}", extension),
                Enumerate => println!("[{}]", extension),
                Credulous(arg) | Skeptical(arg) => {
                    if extension.contains(arg) {
                        println!("YES");
                    } else {
                        println!("NO");
                    }
                },
            }
        },
        Preferred => {
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
            if let FindOne = &problem.task {
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
                match &problem.task {
                    Enumerate => println!("[{}]", preferred.iter()
                        .map(|e| e.to_string())
                        .collect::<Vec<_>>()
                        .join(","),
                    ),
                    Credulous(arg) => {
                        if preferred
                            .iter()
                            .any(|e| e.contains(arg))
                        {
                            println!("YES");
                        } else {
                            println!("NO");
                        }
                    },
                    Skeptical(arg) => {
                        if preferred
                            .iter()
                            .all(|e| e.contains(arg))
                        {
                            println!("YES");
                        } else {
                            println!("NO");
                        }
                    },
                    _ => unreachable!(),
                }
            }
        },
    }
    Ok(())
}
