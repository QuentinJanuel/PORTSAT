use std::fmt;
use super::argument::Argument;

pub struct Attack(pub Argument, pub Argument);

impl fmt::Display for Attack {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{} -> {}", self.0, self.1)
    }
}
