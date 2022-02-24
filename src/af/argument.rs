use std::fmt;

pub struct Argument {
    pub name: String,
    pub attackers: Vec<usize>,
}

impl fmt::Display for Argument {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.name)
    }
}
