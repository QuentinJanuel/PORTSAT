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
    portfolio,
    cnf::{
        Clause,
        Lit,
    },
    solver::{
        Solver,
        minisat::Minisat,
        dpll::DPLL,
    },
};

pub fn solve(
    af: AF,
    problem: Problem,
) -> Result<(), String> {
    let solver = portfolio![
        Minisat::new(),
        DPLL::new(),
    ];
    match &problem.semantics {
        Complete | Stable => {
            let cnf = if let Complete = &problem.semantics {
                af.phi_co()
            } else {
                af.phi_st()
            };
            match &problem.task {
                FindOne => if let Some(model) = solver.solve(&cnf) {
                    println!("{}", Extension::new(&af, &model));
                } else {
                    println!("NO");
                },
                Enumerate => {
                    let models = solver.get_all_models(&cnf);
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
                    if let Some(_) = solver.solve(&cnf) {
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
                    if let Some(_) = solver.solve(&cnf) {
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
