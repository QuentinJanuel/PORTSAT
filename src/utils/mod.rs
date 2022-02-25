pub mod args;
#[macro_use]
pub mod verbose;

use std::{
    fs::File,
    io::Read,
    collections::HashMap,
};
use sat_portfolio::solver::{
    Solver,
    minisat::Minisat,
    manysat::Manysat,
    glucose::Glucose,
    dpll::DPLL,
    portfolio::Portfolio,
};

pub fn read_file(path: &str) -> Result<String, String> {
    let mut file = File::open(path)
        .map_err(|e| format!("{}", e))?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)
        .map_err(|e| format!("{}", e))?;
    Ok(contents)
}

pub fn details() {
    let name = env!("CARGO_PKG_NAME");
    let version = env!("CARGO_PKG_VERSION");
    let author = env!("CARGO_PKG_AUTHORS")
        .split(":")
        .collect::<Vec<_>>()
        .join(", ");
    println!("{} v{}\n{}", name, version, author);
}

pub fn help() {
    println!("Help\nWIP");
}

fn get_all_solvers() -> HashMap<String, Box<dyn Solver + Send>> {
    let mut hashmap: HashMap<_, Box<dyn Solver + Send>> = HashMap::new();
    hashmap.insert(    "minisat".into(), Box::new(Minisat::new()));
    hashmap.insert(    "manysat".into(), Box::new(Manysat::new()));
    hashmap.insert(       "dpll".into(), Box::new(   DPLL::new()));
    hashmap.insert(    "glucose".into(), Box::new(Glucose::new()));
    hashmap.insert("glucose-pre".into(), {
        let mut s = Glucose::new();
        s.enable_preprocessing();
        Box::new(s)
    });
    hashmap
}

pub fn show_available_solvers() {
    let solvers = get_all_solvers();
    let s = solvers.iter()
        .map(|(name, _)| name.clone())
        .collect::<Vec<String>>()
        .join(",");
    println!("[{}]", s);
}

pub fn get_solvers_from_arg(arg: Option<&str>) -> Box<dyn Solver> {
    if let Some(solver_names) = arg {
        let mut solvers: Vec<Box<dyn Solver + Send>> = vec![];
        let all_solvers = get_all_solvers();
        for solver_name in solver_names.split(',') {
            if let Some(solver) = all_solvers.get(solver_name) {
                solvers.push(solver.clone());
            } else {
                panic!("Unknown solver: {}", solver_name);
            }
        }
        if solvers.len() < 1 {
            panic!("No solver specified");
        }
        Box::new(Portfolio::from(solvers))
    } else {
        // Default solver: manysat
        Box::new(Manysat::new())
    }
}
