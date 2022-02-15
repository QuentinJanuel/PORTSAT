mod argument;
mod attack;

use std::fmt;
pub use argument::Argument;
pub use attack::Attack;
use crate::{
    problem::{
        Problem,
        Semantics,
        Task,
    },
};
use sat_portfolio::cnf::{
    CNF,
    Clause,
    Lit,
    Var,
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
    pub fn phi_st(&self) -> CNF {
        let mut cnf = CNF::new();
        for (ind_a, a) in self.arguments.iter().enumerate() {
            let mut clause1 = Clause::new();
            let var_a = Var(ind_a as u32);
            clause1.add(Lit::pos(var_a));
            for (ind_b, b) in self.arguments.iter().enumerate() {
                let b_attacks_a = self.attacks.iter()
                        .any(|att| att.0 == *b && att.1 == *a);
                if !b_attacks_a {
                    continue;
                }
                let var_b = Var(ind_b as u32);
                clause1.add(Lit::pos(var_b));
                let mut clause2 = Clause::new();
                clause2.add(Lit::neg(var_a));
                clause2.add(Lit::neg(var_b));
                cnf.add_clause(clause2);
            }
            cnf.add_clause(clause1);
        }
        cnf
    }
    pub fn phi_co(&self) -> CNF {
        let cnf = CNF::new();
        cnf
    }
    pub fn phi(&self, problem: &Problem) -> CNF {
        let base = match problem.semantics {
            Semantics::Stable => self.phi_st(),
            _ => self.phi_co(),
        };
        base
        // match &problem.task {
        //     Task::Credulous(param) => LF::And(vec![
        //         base,
        //         LF::Atom(param.to_string()),
        //     ]),
        //     Task::Skeptical(param) => LF::And(vec![
        //         base,
        //         LF::Not(Box::new(
        //             LF::Atom(param.to_string()),
        //         )),
        //     ]),
        //     _ => base,
        // }
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
