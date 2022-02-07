use std::fmt;

#[derive(PartialEq, Clone)]
pub struct Argument(pub String);

impl fmt::Display for Argument {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}
