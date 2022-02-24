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
use std::time::Instant;
use sat_portfolio::{
    cnf::{
        Clause,
        Lit,
    },
    solver::Solver,
};

pub fn solve(
    af: AF,
    problem: Problem,
    sat_solver: Box<dyn Solver>,
) -> Result<(), String> {
    match &problem.semantics {
        Complete | Stable => {
            log!("Generating SAT instance...");
            let now = Instant::now();
            let cnf = if let Complete = &problem.semantics {
                af.phi_co()
            } else {
                af.phi_st()
            };
            log!("Generated in {}ms", now.elapsed().as_millis());
            match &problem.task {
                FindOne => {
                    log!("Solving SAT instance...");
                    let now = Instant::now();
                    if let Some(model) = sat_solver.solve(&cnf) {
                        println!("{}", Extension::new(&af, &model));
                    } else {
                        println!("NO");
                    }
                    log!("Done in {}ms", now.elapsed().as_millis());
                },
                Enumerate => {
                    let models = sat_solver.get_all_models(&cnf);
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
                    if let Some(_) = sat_solver.solve(&cnf) {
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
                    if let Some(_) = sat_solver.solve(&cnf) {
                        println!("NO");
                    } else {
                        println!("YES");
                    }
                },
            }
        },
        Grounded => unimplemented!("Grounded"),
        Preferred => unimplemented!("Preferred"),
    }
    Ok(())
}
