use std::{
    fmt,
    str::FromStr,
};

#[derive(Clone)]
pub enum Task {
    Credulous,
    Skeptical,
    Enumerate,
    FindOne,
}

impl fmt::Display for Task {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::Credulous => write!(f, "DC"),
            Self::Skeptical => write!(f, "DS"),
            Self::Enumerate => write!(f, "EE"),
            Self::FindOne => write!(f, "SE"),
        }
    }
}

impl FromStr for Task {
    type Err = ();
    fn from_str(input: &str) -> Result<Self, Self::Err> {
        match input {
            "DC" => Ok(Self::Credulous),
            "DS" => Ok(Self::Skeptical),
            "EE" => Ok(Self::Enumerate),
            "SE" => Ok(Self::FindOne),
            _ => Err(()),
        }
    }
}
