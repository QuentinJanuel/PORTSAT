mod logic;
mod af;

use af::AF;

fn main() {
    let af = AF::from(
        vec!["a", "b", "c", "d", "e"],
        vec![
            ("a", "b"),
            ("b", "a"),
            ("b", "c"),
            ("c", "d"),
            ("d", "e"),
            ("e", "c"),
        ],
    );
    println!("{}", af.to_cnf());
}
