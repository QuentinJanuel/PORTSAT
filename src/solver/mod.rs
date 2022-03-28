mod benchmark;
mod stable_complete;
mod grounded;
mod preferred;

use crate::{
    af::AF,
    problem::{
        Problem,
        Semantics,
    },
};
use sat_portfolio::solver::Solver;

pub fn solve(
    af: AF,
    problem: Problem,
    sat_solver: Option<Box<dyn Solver>>,
) -> Result<(), String> {
    match &problem.semantics {
        Semantics::Complete => {
            stable_complete::solve(
                &af,
                || af.phi_co(),
                &problem.task,
                sat_solver,
            )
        },
        Semantics::Stable => {
            stable_complete::solve(
                &af,
                || af.phi_st(),
                &problem.task,
                sat_solver,
            )
        },
        Semantics::Grounded =>
            grounded::solve(&af, &problem.task, sat_solver)?,
        Semantics::Preferred =>
            preferred::solve(&af, &problem.task, sat_solver),
    }
    Ok(())
}
