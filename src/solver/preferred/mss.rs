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
    let cnf = benchmark!(
        BenchmarkTask::CNFGeneration,
        af.phi_co(),
    );
    benchmark!(BenchmarkTask::SATSolving, {
        let mut model = sat_solver.solve(&cnf)
            .unwrap_or_else(||
                panic!("There should always exist at least one preferred extension")
            );
        match task {
            Task::FindOne => {
                // cargo run --release -- -p SE-PR -fo tgf -f experiments/utils/iccma/data/testset1_gr_small/g_34388__1224__1_1_1__1618570817.tgf -s maplesat -v
                let mut pos_vars = model.get_pos_vars();
                let neg_vars = model.get_neg_vars();
                let neg_vars = neg_vars.into_iter()
                    .filter(|var|
                        af.arguments.get(var.0 as usize).is_some()
                    )
                    .collect::<Vec<_>>();
                for var in neg_vars.iter() {
                    let lit = model.get_lit_mut(var.clone()).unwrap();
                    *lit = lit.not();
                    pos_vars.push(lit.get_var());
                    let ok = cnf.get_clauses()
                        .iter()
                        .all(|c|
                            !c.contains_var(lit.get_var()) ||
                            c.get_lits()
                                .iter()
                                .any(|l| {
                                    let is_in_model = pos_vars.contains(&l.get_var());
                                    l.get_sign() == is_in_model
                                })
                        );
                    if !ok {
                        *lit = lit.not();
                        pos_vars.pop();
                    }
                }
                println!("{}", Extension::new(&af, &model));
            },
            Task::Enumerate => unimplemented!(),
            Task::Credulous(_arg) => unimplemented!(),
            Task::Skeptical(_arg) => unimplemented!(),
        };
    });
}
