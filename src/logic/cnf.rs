use std::fmt;
use super::Clause;

pub struct CNF(pub Vec<Clause>);

impl fmt::Display for CNF {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let s = self.0
            .iter()
            .map(|clause| format!("{}", clause))
            .collect::<Vec<String>>()
            .join("\n");
        write!(f, "{}", s)
    }
}
