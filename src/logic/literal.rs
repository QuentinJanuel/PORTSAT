use std::fmt;

pub enum Literal {
    Pos(String),
    Neg(String),
}

impl fmt::Display for Literal {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Literal::Pos(s) => write!(f, "{}", s),
            Literal::Neg(s) => write!(f, "-{}", s),
        }
    }
}
