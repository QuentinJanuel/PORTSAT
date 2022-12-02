mod enum_co;
mod mss;

use crate::{
    af::AF,
    problem::Task,
};
use sat_portfolio::solver::Solver;

pub fn solve(
    af: &AF,
    task: &Task,
    sat_solver: Option<Box<dyn Solver>>,
    // mss: bool,
) {
    match task {
        Task::FindOne => mss::solve(af, task, sat_solver),
        _ => enum_co::solve(af, task, sat_solver),
    }
    // if mss {
    //     mss::solve(af, task, sat_solver),
    // } else {
    //     enum_co::solve(af, task, sat_solver)
    // }
}