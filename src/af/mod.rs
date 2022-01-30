mod argument;
mod attack;

use std::fmt;
pub use argument::Argument;
pub use attack::Attack;
use crate::logic::{
    CNF,
    Clause,
    Literal,
};

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
    pub fn to_cnf(&self) -> CNF {
        let mut cnf = CNF(vec![]);
        for attack in self.attacks.iter() {
            let attacker = &attack.0;
            let attacked = &attack.1;
            let lit = Literal::Pos(
                format!("attack_{}_{}", attacker, attacked),
            );
            cnf.0.push(Clause(vec![lit]));
        }
        for arg1 in self.arguments.iter() {
            let clause1 = Clause(vec![
                Literal::Pos(format!("acc_{}", arg1)),
                Literal::Pos(format!("def_{}", arg1)),
            ]);
            cnf.0.push(clause1);
            let clause2 = Clause(vec![
                Literal::Neg(format!("acc_{}", arg1)),
                Literal::Neg(format!("def_{}", arg1)),
            ]);
            cnf.0.push(clause2);
            for arg2 in self.arguments.iter() {
                let clause3 = Clause(vec![
                    Literal::Pos(format!("def_{}", arg1)),
                    Literal::Neg(format!("attack_{}_{}", arg2, arg1)),
                    Literal::Neg(format!("acc_{}", arg2)),
                ]);
                cnf.0.push(clause3);
            }
        }
        cnf
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
