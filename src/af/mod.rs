mod argument;
mod attack;

use std::fmt;
pub use argument::Argument;
pub use attack::Attack;
use crate::{
    problem::{
        Problem,
        Semantics,
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
    fn has_attack(&self, from: &Argument, to: &Argument) -> bool {
        self.attacks.iter()
            .any(|a| a.0 == *from && a.1 == *to)
    }
    pub fn get_var(&self, arg: &Argument) -> Var {
        let index = self.arguments
            .iter()
            .position(|a| a == arg)
            .unwrap();
        Var(index as u32)
    }
    fn get_p_var(&self, arg: &Argument) -> Var {
        let mut var = self.get_var(arg);
        var.0 += self.arguments.len() as u32;
        var
    }
    pub fn get_arg(&self, var: &Var) -> Option<&Argument> {
        let index = var.0 as usize;
        self.arguments.get(index)
    }
    pub fn phi_st(&self) -> CNF {
        let mut cnf = CNF::new();
        for a in self.arguments.iter() {
            let mut clause1 = Clause::new();
            let var_a = self.get_var(a);
            clause1.add(Lit::pos(var_a));
            for b in self.arguments.iter()  {
                if !self.has_attack(b, a) {
                    continue;
                }
                let var_b = self.get_var(b);
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
        let mut cnf = CNF::new();
        for a in self.arguments.iter() {
            let var_a = self.get_var(a);
            let var_p_a = self.get_p_var(a);
            // Clause 1
            let mut clause1 = Clause::new();
            clause1.add(Lit::neg(var_a));
            clause1.add(Lit::neg(var_p_a));
            cnf.add_clause(clause1);
            // 
            // Clause 2
            let mut clause2 = Clause::new();
            clause2.add(Lit::pos(var_a));
            // 
            // Clause 4
            let mut clause4 = Clause::new();
            clause4.add(Lit::neg(var_p_a));
            // 
            for b in self.arguments.iter() {
                if !self.has_attack(b, a) {
                    continue;
                }
                let var_b = self.get_var(b);
                let var_p_b = self.get_p_var(b);
                // Clause 2
                clause2.add(Lit::neg(var_p_b));
                // 
                // Clause 3
                let mut clause3 = Clause::new();
                clause3.add(Lit::neg(var_a));
                clause3.add(Lit::pos(var_p_b));
                cnf.add_clause(clause3);
                // 
                // Clause 4
                clause4.add(Lit::pos(var_b));
                // 
                // Clause 5
                let mut clause5 = Clause::new();
                clause5.add(Lit::pos(var_p_a));
                clause5.add(Lit::neg(var_b));
                cnf.add_clause(clause5);
                // 
            }
            // Clause 2
            cnf.add_clause(clause2);
            // 
            // Clause 4
            cnf.add_clause(clause4);
            // 
        }
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
