mod af;
mod utils;
mod problem;
mod solver;

use af::AF;
use utils::args::Args;
use std::convert::TryInto;
use solver::solve;

fn main() -> Result<(), String> {
    let args = Args::new();
    if args.has("--problems") {
        problem::all_problems();
    } else if args.has("--formats") {
        println!("[tgf]");
    } else if let Some(problem) = args.get("-p") {
        let param = args.get("-a");
        let problem = (problem, param).try_into()?;
        let file = args.get("-f")
            .ok_or("The file is not specified")?;
        let tgf = utils::read_file(file)?;
        let af = AF::from_tgf(&tgf);
        solve(af, problem)?;
    } else {
        utils::details();
    }
    Ok(())
}
