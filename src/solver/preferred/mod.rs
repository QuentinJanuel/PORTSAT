mod enum_co;
mod fill;

use crate::{
    af::AF,
    problem::Task,
};
use sat_portfolio::solver::Solver;

pub fn solve(
    af: &AF,
    task: &Task,
    sat_solver: Option<Box<dyn Solver>>,
) {
    if true {
        enum_co::solve(af, task, sat_solver)
    } else {
        fill::solve(af, task, sat_solver)
    }
}