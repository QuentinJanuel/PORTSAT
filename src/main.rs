mod af;
mod utils;
mod problem;

use af::AF;
use utils::args::Args;
use std::convert::TryInto;
use sat_portfolio::{
    portfolio,
    solver::{
        Solver,
        minisat::Minisat,
        dpll::DPLL,
    },
};

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
        let cnf = af.phi(&problem);
        let solver = portfolio![
            Minisat::new(),
            DPLL::new(),
        ];
        let models = solver.get_all_models(&cnf);
        // Some(&af.arguments.iter()
        //     .map(|arg| af.get_var(arg))
        //     .collect()),
        for model in &models {
            println!("Extension found:");
            model.get_pos_vars().iter()
                .filter_map(|var| af.get_arg(&var))
                .for_each(|arg| println!("{}", arg));
        }
        if models.is_empty() {
            println!("No solution");
        }
    } else {
        utils::details();
    }
    Ok(())
}
