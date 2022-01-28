use std::fmt;
use super::Literal;

pub struct Clause(pub Vec<Literal>);

impl fmt::Display for Clause {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let s = self.0
            .iter()
            .map(|literal| format!("{}", literal))
            .collect::<Vec<String>>()
            .join(" ");
        write!(f, "{}", s)
    }
}
