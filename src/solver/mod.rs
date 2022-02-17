use crate::{
    af::{
        AF,
        Extension,
    },
    problem::Problem,
    problem::{
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
        config::ConfigAll,
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
                    let vars = af.arguments.iter()
                        .map(|arg| af.get_var(arg))
                        .collect::<Vec<_>>();
                    let config = if let Complete = &problem.semantics {
                        ConfigAll::default().with_vars(&vars)
                    } else {
                        ConfigAll::default()
                    };
                    let models = solver.get_all_models_with_config(
                        &cnf,
                        &config,
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
        Grounded => panic!("Grounded not supported yet"),
        Preferred => panic!("Preferred not supported yet"),
    }
    Ok(())
}
