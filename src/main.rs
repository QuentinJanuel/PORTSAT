#[macro_use]
extern crate lalrpop_util;

mod af;
#[macro_use]
mod utils;
mod problem;
mod solver;

use af::{
    AF,
    format::Format,
};
use problem::Semantics;
use utils::{
    args::Args,
    solvers,
    verbose::VERBOSE,
};
use std::{convert::TryInto, str::FromStr};
use solver::solve;

use crate::problem::Problem;

fn main() -> Result<(), String> {
    let args = Args::new();
    if args.has("-v") {
        VERBOSE.enable();
    }
    if args.has("-h") {
        utils::help();
    } else if args.has("--problems") {
        problem::all_problems();
    } else if args.has("--formats") {
        Format::show_available();
    } else if args.has("--solvers") {
        solvers::show_available();
    } else if let Some(problem) = args.get("-p") {
        let param = args.get("-a");
        let problem: Problem = (problem, param).try_into()?;
        let file = args.get("-f")
            .ok_or("The file is not specified")?;
        let format = Format::from_str(
            args.get("-fo")
                .unwrap_or("paf")
                // .ok_or("The format is not specified")?
        )?;
        let file = utils::read_file(file)?;
        let af = benchmark!(
            format!("{} parsing", format.to_string().to_uppercase()),
            match format {
                Format::TGF => AF::from_tgf(&file),
                Format::APX => AF::from_apx(&file),
                Format::LooseAPX => AF::from_loose_apx(&file),
                Format::PAF => AF::from_paf(&file),
            },
        );
        let is_gr = problem.semantics == Semantics::Grounded;
        solve(
            af,
            problem,
            solvers::get_from_arg(/*args.get("-s"),*/ is_gr),
            // args.has("--pr-mss"),
        )?;
    } else {
        utils::details();
    }
    Ok(())
}
