mod logic;
mod af;
mod utils;
mod problem;

use af::AF;

fn details() {
    let name = env!("CARGO_PKG_NAME");
    let version = env!("CARGO_PKG_VERSION");
    let author = env!("CARGO_PKG_AUTHORS")
        .split(":")
        .collect::<Vec<_>>()
        .join(", ");
    println!("{} v{}\n{}", name, version, author);
}

fn main() {
    details();
    let tgf = utils::read_file("examples/tgf.txt");
    let af = AF::from_tgf(&tgf);
    println!("{}", af);
    problem::all_problems();
}
