mod argument;
mod attack;

use std::fmt;
pub use argument::Argument;
pub use attack::Attack;
use crate::{
    lf::LF,
    problem::{
        Problem,
        Semantics,
        Task,
    },
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
    fn phi_cf(&self) -> LF {
        let attacks = self.attacks
            .iter()
            .map(|attack| {
                let a = LF::Atom(attack.0.to_string());
                let b = LF::Atom(attack.1.to_string());
                let conj = LF::And(vec![a, b]);
                LF::Not(Box::new(conj))
            })
            .collect();
        LF::And(attacks)
    }
    pub fn phi_st(&self) -> LF {
        let args = self.arguments
            .iter()
            .map(|a| {
                let atom = LF::Atom(a.to_string());
                let conj = self.attacks
                    .iter()
                    .filter(|attack| &attack.1 == a)
                    .map(|attack| {
                        let b = LF::Atom(attack.0.to_string());
                        LF::Not(Box::new(b))
                    })
                    .collect();
                let conj = LF::And(conj);
                LF::Equiv(Box::new(atom), Box::new(conj))
            })
            .collect();
        LF::And(args)
    }
    pub fn phi_co(&self) -> LF {
        let mut args: Vec<LF> = self.arguments
            .iter()
            .map(|a| {
                let atom_a = LF::Atom(a.to_string());
                let conj = self.attacks
                    .iter()
                    .filter(|att1| &att1.1 == a)
                    .map(|att1| {
                        let b = &att1.0;
                        let disj = self.attacks
                            .iter()
                            .filter(|att2| &att2.1 == b)
                            .map(|att2| {
                                let c = &att2.0;
                                let atom_c = LF::Atom(c.to_string());
                                atom_c
                            })
                            .collect();
                        let disj = LF::Or(disj);
                        disj
                    })
                    .collect();
                let conj = LF::And(conj);
                LF::Equiv(Box::new(atom_a), Box::new(conj))
            })
            .collect();
        args.push(self.phi_cf());
        LF::And(args)
    }
    pub fn phi(&self, problem: &Problem, param: &str) -> LF {
        let base = match problem.semantics {
            Semantics::Stable => self.phi_st(),
            _ => self.phi_co(),
        };
        match problem.task {
            Task::Credulous => LF::And(vec![
                base,
                LF::Atom(param.to_string()),
            ]),
            Task::Skeptical => LF::And(vec![
                base,
                LF::Not(Box::new(
                    LF::Atom(param.to_string()),
                )),
            ]),
            _ => base,
        }
    }
}

impl fmt::Display for AF {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "{}\n{}",
            self.arguments
                .iter()
                .map(Argument::to_string)
                .collect::<Vec<_>>()
                .join("\n"),
            self.attacks
                .iter()
                .map(Attack::to_string)
                .collect::<Vec<_>>()
                .join("\n"),
        )
    }
}
