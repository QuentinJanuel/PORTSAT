use std::fmt;

// Logical Formula
pub enum LF {
    Atom(String),
    Not(Box<LF>),
    And(Vec<LF>),
    Or(Vec<LF>),
    Equiv(Box<LF>, Box<LF>),
}

impl fmt::Display for LF {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::Atom(s) => write!(f, "{}", s),
            Self::Not(lf) => write!(f, "!{}", lf),
            Self::And(lfs) => write!(
                f,
                "({})",
                lfs.iter()
                    .map(Self::to_string)
                    .collect::<Vec<_>>()
                    .join(" && ")
            ),
            Self::Or(lfs) => write!(
                f,
                "({})",
                lfs.iter()
                    .map(Self::to_string)
                    .collect::<Vec<_>>()
                    .join(" || ")
            ),
            Self::Equiv(lf1, lf2) => write!(
                f,
                "({} <=> {})",
                Self::to_string(lf1),
                Self::to_string(lf2)
            ),
        }
    }
}
