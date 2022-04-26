use crate::{
    af::{
        AF,
        Extension,
    },
    problem::Task,
};
use sat_portfolio::{solver::Solver, cnf::Clause};
use super::super::benchmark::BenchmarkTask;

pub fn solve(
    af: &AF,
    task: &Task,
    sat_solver: Option<Box<dyn Solver>>,
) {
    let sat_solver = sat_solver
        .unwrap_or_else(|| Box::new(sat_portfolio::solver::manysat::Manysat::new()));
    match task {
        Task::FindOne => {
            // cargo run --release -- -p SE-PR -fo tgf -f experiments/utils/iccma/data/testset1_gr_small/g_34388__1224__1_1_1__1618570817.tgf -s maplesat -v
            let mut cnf = benchmark!(
                BenchmarkTask::CNFGeneration,
                af.phi_co(),
            );
            benchmark!(BenchmarkTask::SATSolving, {
                let mut model = sat_solver.solve(&cnf)
                    .unwrap_or_else(||
                        panic!("There should always exist at least one preferred extension")
                    );
                loop {
                    let lits = model.get_literals()
                        .iter()
                        .filter_map(|l| if l.get_sign() {
                            None
                        } else {
                            Some(l.not())
                        })
                        .collect::<Vec<_>>();
                    let clause = Clause::from(lits);
                    cnf.add_clause(clause);
                    for lit in model.get_literals() {
                        if lit.get_sign() {
                            let clause = Clause::from(vec![*lit]);
                            cnf.add_clause(clause);
                        }
                    }
                    let new_model = sat_solver.solve(&cnf);
                    if let Some(new_model) = new_model {
                        model = new_model;
                    } else {
                        break;
                    }
                }
                println!("{}", Extension::new(&af, &model));
            });
        },
        Task::Enumerate => unimplemented!(),
        Task::Credulous(_arg) => unimplemented!(),
        Task::Skeptical(_arg) => unimplemented!(),
    };
}
