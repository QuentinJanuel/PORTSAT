use std::{
    fmt,
    convert::From,
};
use crate::af::Argument;

#[derive(Clone)]
pub enum Task {
    Credulous(Argument),
    Skeptical(Argument),
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

impl From<(&str, Option<&str>)> for Task {
    fn from((task, arg): (&str, Option<&str>)) -> Self {
        let arg = arg.map(|arg| Argument(arg.to_string()));
        match (task, arg) {
            ("DC", Some(arg)) => Self::Credulous(arg),
            ("DS", Some(arg)) => Self::Skeptical(arg),
            ("DC", None) => panic!("The argument is not specified"),
            ("DS", None) => panic!("The argument is not specified"),
            ("EE", _) => Self::Enumerate,
            ("SE", _) => Self::FindOne,
            _ => panic!("Invalid task"),
        }
    }
}
