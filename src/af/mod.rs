mod argument;
mod attack;

use std::fmt;
pub use argument::Argument;
pub use attack::Attack;
use crate::{
    lf::LF,
    problem::Semantics,
};

// Argumentation Framework
pub struct AF {
    pub arguments: Vec<Argument>,
    pub attacks: Vec<Attack>,
}

impl AF {
    fn from(args: Vec<&str>, attacks: Vec<(&str, &str)>) -> Self {
        Self {
            arguments: args
                .iter()
                .map(|&arg| Argument(arg.to_string()))
                .collect(),
            attacks: attacks
                .iter()
                .map(|&(a, b)| Attack(
                    Argument(a.to_string()),
                    Argument(b.to_string()),
                ))
                .collect(),
        }
    }
    pub fn from_tgf(tgf: &str) -> Self {
        let arg_att = tgf.split("#").collect::<Vec<_>>();
        let args = arg_att[0]
            .lines()
            .filter(|&s| !s.is_empty())
            .map(|s| s.split(" ").next().unwrap())
            .collect::<Vec<_>>();
        let attacks = arg_att[1]
            .lines()
            .filter(|&s| !s.is_empty())
            .map(|s| {
                let mut iter = s.split(" ");
                (
                    iter.next().unwrap(),
                    iter.next().unwrap(),
                )
            })
            .collect::<Vec<_>>();
        Self::from(args, attacks)
    }
    pub fn phi(&self, semantics: &Semantics) -> LF {
        LF::Atom("hello".to_string())
    }
}

impl fmt::Display for AF {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "{}\n{}",
            self.arguments
                .iter()
                .map(|arg| format!("{}", arg))
                .collect::<Vec<_>>()
                .join("\n"),
            self.attacks
                .iter()
                .map(|attack| format!("{}", attack))
                .collect::<Vec<_>>()
                .join("\n"),
        )
    }
}
