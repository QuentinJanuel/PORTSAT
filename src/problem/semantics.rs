use std::{
    fmt,
    str::FromStr,
};

#[derive(Clone)]
pub enum Semantics {
    Complete,
    Grounded,
    Preferred,
    Stable,
}

impl fmt::Display for Semantics {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::Complete => write!(f, "CO"),
            Self::Grounded => write!(f, "GR"),
            Self::Preferred => write!(f, "PR"),
            Self::Stable => write!(f, "ST"),
        }
    }
}

impl FromStr for Semantics {
    type Err = ();
    fn from_str(input: &str) -> Result<Self, Self::Err> {
        match input {
            "CO" => Ok(Self::Complete),
            "GR" => Ok(Self::Grounded),
            "PR" => Ok(Self::Preferred),
            "ST" => Ok(Self::Stable),
            _ => Err(()),
        }
    }
}
