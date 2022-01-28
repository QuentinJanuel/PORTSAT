mod logic;
mod af;

use af::AF;

fn main() {
    let af = AF::from(
        vec!["a", "b"],
        vec![
            ("a", "b"),
            ("b", "a"),
        ],
    );
    println!("{}", af.to_cnf());
}
