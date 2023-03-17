pub mod args;
#[macro_use]
pub mod verbose;
pub mod solvers;

use std::{
    fs::File,
    io::Read,
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
        .join("\n");
    println!("{} v{}\n{}", name, version, author);
}

pub fn help() {
    println!(r#"
Help:
-h
    Show this help message.
-v
    Show more information.
--problems
    Show all available problems.
--formats
    Show all available formats.
--solvers
    Show all available solvers.
-s <solver>
    Specify the solver to use.
-fo <format>
    Specify the format of the input file.
    The format is one of the following:
        - tgf
        - apx
        - loose-apx
        - paf
    The default format is paf.
-f <file>
    Specify the file to read.
-p <problem>
    Specify the problem to solve as <task>-<semantics>.
    The task is one of the following:
        - DC (decide credulous)
        - DS (decide skeptical)
        - SE (find some extension)
    The semantics is one of the following:
        - CO (complete)
        - GR (grounded)
        - PR (preferred)
        - ST (stable)
-a <param>
    Specify the parameter for the decide problems.
    "#);
}
