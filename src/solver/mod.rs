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
    solver::Solver,
};

pub fn solve(
    af: AF,
    problem: Problem,
    sat_solver: Box<dyn Solver>,
) -> Result<(), String> {
    match &problem.semantics {
        Complete | Stable => {
            let cnf = benchmark!("CNF generation", {
                if let Complete = &problem.semantics {
                    af.phi_co()
                } else {
                    af.phi_st()
                }
            });
            match &problem.task {
                FindOne => {
                    let model = benchmark!("SAT solving", {
                        sat_solver.solve(&cnf)
                    });
                    if let Some(model) = model {
                        println!("{}", Extension::new(&af, &model));
                    } else {
                        println!("NO");
                    }
                },
                Enumerate => {
                    let mut cnf = cnf;
                    let models = sat_solver.get_all_models(&mut cnf);
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
