use std::{
    fmt,
    convert::TryFrom,
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

impl TryFrom<&str> for Semantics {
    type Error = &'static str;
    fn try_from(input: &str) -> Result<Self, Self::Error> {
        match input {
            "CO" => Ok(Self::Complete),
            "GR" => Ok(Self::Grounded),
            "PR" => Ok(Self::Preferred),
            "ST" => Ok(Self::Stable),
            _ => Err("Invalid semantics"),
        }
    }
}
