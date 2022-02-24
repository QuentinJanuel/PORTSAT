use std::{
    fmt,
    convert::TryFrom,
};

#[derive(Clone)]
pub enum Task {
    Credulous(String),
    Skeptical(String),
    Enumerate,
    FindOne,
}

impl fmt::Display for Task {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::Credulous(_) => write!(f, "DC"),
            Self::Skeptical(_) => write!(f, "DS"),
            Self::Enumerate => write!(f, "EE"),
            Self::FindOne => write!(f, "SE"),
        }
    }
}

impl TryFrom<(&str, Option<&str>)> for Task {
    type Error = &'static str;
    fn try_from((task, arg): (&str, Option<&str>)) -> Result<Self, Self::Error> {
        match (task, arg) {
            ("DC", Some(arg)) => Ok(Self::Credulous(arg.into())),
            ("DS", Some(arg)) => Ok(Self::Skeptical(arg.into())),
            ("DC", None) => Err("The argument is not specified"),
            ("DS", None) => Err("The argument is not specified"),
            ("EE", _) => Ok(Self::Enumerate),
            ("SE", _) => Ok(Self::FindOne),
            _ => Err("Invalid task"),
        }
    }
}
