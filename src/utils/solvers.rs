use std::{
    collections::HashMap,
    sync::Arc,
};
use sat_portfolio::solver::{
    Solver,
    minisat::Minisat,
    manysat::Manysat,
    maplesat::Maplesat,
    glucose::Glucose,
    dpll::DPLL,
    portfolio::Portfolio,
};

type SolverGen = fn() -> Box<dyn Solver>;

fn get_all() -> HashMap<String, SolverGen> {
    let mut hashmap: HashMap<_, SolverGen> = HashMap::new();
    hashmap.insert(    "minisat".into(), || Box::new( Minisat::new()));
    hashmap.insert(    "manysat".into(), || Box::new( Manysat::new()));
    hashmap.insert(   "maplesat".into(), || Box::new(Maplesat::new()));
    hashmap.insert(       "dpll".into(), || Box::new(    DPLL::new()));
    hashmap.insert(    "glucose".into(), || Box::new( Glucose::new()));
    hashmap.insert("glucose-pre".into(), || {
        let mut s = Glucose::new();
        s.enable_preprocessing();
        Box::new(s)
    });
    // {
    //     #[cfg(not(target_os = "windows"))]
    //     hashmap.insert("glucose-syrup".into(), || {
    //         let mut s = Glucose::new();
    //         s.enable_syrup();
    //         Box::new(s)
    //     });
    // }
    hashmap
}

pub fn show_available() {
    let solvers = get_all();
    let s = solvers.iter()
        .map(|(name, _)| name.clone())
        .collect::<Vec<String>>()
        .join(",");
    println!("[{}]", s);
}

fn get_default(is_gr: bool) -> Option<Box<dyn Solver>> {
    if is_gr {
        None
    } else {
        Some(Box::new(Portfolio::from(vec![
            Arc::new(Manysat::new()),
            Arc::new(Minisat::new()),
            Arc::new(Maplesat::new()),
            Arc::new(Glucose::new()),
            Arc::new({
                let mut s = Glucose::new();
                s.enable_preprocessing();
                s
            }),
        ])))
    }
}

pub fn get_from_arg(arg: Option<&str>, is_gr: bool) -> Option<Box<dyn Solver>> {
    arg.map(|solver_names| {
        let mut solvers: Vec<Arc<dyn Solver>> = vec![];
        let all_solvers = get_all();
        for solver_name in solver_names.split(',') {
            if let Some(solver_gen) = all_solvers.get(solver_name) {
                solvers.push(solver_gen().into());
            } else {
                panic!("Unknown solver: {}", solver_name);
            }
        }
        if solvers.len() < 1 {
            panic!("No solver specified");
        }
        Box::new(Portfolio::from(solvers)) as Box<dyn Solver>
    }).or_else(|| get_default(is_gr))
}
