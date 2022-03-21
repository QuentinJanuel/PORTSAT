mod argument;
mod attack;
mod extension;
pub mod format;

use std::{
    fmt,
    collections::HashMap,
};
pub use argument::Argument;
pub use attack::Attack;
pub use extension::Extension;
use sat_portfolio::cnf::{
    CNF,
    Clause,
    Lit,
    Var,
};

lalrpop_mod!(pub apx_parser, "/af/apx.rs");

// Argumentation Framework
pub struct AF {
    pub arguments: Vec<Argument>,
}

impl AF {
    pub fn get_var(&self, arg_name: &str) -> Var {
        let index = self.arguments
            .iter()
            .position(|a| a.name == arg_name)
            .unwrap_or_else(|| panic!("Unexisting argument"));
        Var(index as u32)
    }
    pub fn from_loose_apx(apx: &str) -> Self {
        let parser = apx_parser::APXParser::new();
        let (
            s_args,
            s_atts,
        ) = parser.parse(apx).unwrap();
        let mut hm: HashMap<&str, usize> = HashMap::new();
        let mut arguments = vec![];
        for name in &s_args {
            let arg = Argument {
                name: name.into(),
                attackers: vec![],
            };
            hm.insert(name, arguments.len());
            arguments.push(arg);
        }
        for (a, b) in &s_atts {
            let a_ind = *hm.get(a.as_str()).unwrap();
            let b_ind = *hm.get(b.as_str()).unwrap();
            arguments[b_ind].attackers.push(a_ind);
        }
        Self { arguments }
    }
    pub fn from_apx(apx: &str) -> Self {
        let mut hm: HashMap<&str, usize> = HashMap::new();
        let mut arguments = vec![];
        let mut in_attacks = false;
        for s in apx.lines() {
            let s = s.trim();
            if s.is_empty() {
                continue
            }
            if !in_attacks && &s[1..=1] == "t" {
                in_attacks = true;
            }
            if !in_attacks {
                let name = &s[4..s.len() - 2];
                let arg = Argument {
                    name: name.into(),
                    attackers: vec![],
                };
                hm.insert(name, arguments.len());
                arguments.push(arg);
            } else {
                let args = &s[4..s.len() - 2];
                let mut args = args.split(",");
                let (a, b) = (
                    args.next().unwrap(),
                    args.next().unwrap(),
                );
                let a_ind = *hm.get(a).unwrap();
                let b_ind = *hm.get(b).unwrap();
                arguments[b_ind].attackers.push(a_ind);
            }
        }
        Self { arguments }
    }
    pub fn from_tgf(tgf: &str) -> Self {
        let arg_att = tgf.split("#").collect::<Vec<_>>();
        let mut hm: HashMap<&str, usize> = HashMap::new();
        let mut arguments = vec![];
        for s in arg_att[0].lines() {
            if s.is_empty() {
                continue
            }
            let name = s.split(" ")
                .next()
                .unwrap();
            let arg = Argument {
                name: name.into(),
                attackers: vec![],
            };
            hm.insert(name, arguments.len());
            arguments.push(arg);
        }
        for s in arg_att[1].lines() {
            if s.is_empty() {
                continue;
            }
            let mut iter = s.split(" ");
            let (a, b) = (
                iter.next().unwrap(),
                iter.next().unwrap(),
            );
            let a_ind = *hm.get(a).unwrap();
            let b_ind = *hm.get(b).unwrap();
            arguments[b_ind].attackers.push(a_ind);
        }
        Self { arguments }
    }
    pub fn phi_co(&self) -> CNF {
        let mut cnf = CNF::new();
        let len = self.arguments.len();
        for (a_ind, a) in self.arguments.iter().enumerate() {
            let var_a = Var(a_ind as u32);
            let var_p_a = Var((a_ind + len) as u32);
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
            for b_ind in &a.attackers {
                let var_b = Var(*b_ind as u32);
                let var_p_b = Var((*b_ind + len) as u32);
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
    pub fn phi_st(&self) -> CNF {
        let mut cnf = CNF::new();
        for (a_ind, a) in self.arguments.iter().enumerate() {
            let var_a = Var(a_ind as u32);
            let mut clause1 = Clause::from(vec![Lit::pos(var_a)]);
            for b_ind in &a.attackers {
                let var_b = Var(*b_ind as u32);
                clause1.add(Lit::pos(var_b));
                cnf.add_clause(Clause::from(vec![
                    Lit::neg(var_a),
                    Lit::neg(var_b),
                ]));
            }
            cnf.add_clause(clause1);
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
                .map(Argument::to_string)
                .collect::<Vec<_>>()
                .join("\n"),
            self.arguments
                .iter()
                .flat_map(|b| {
                    let mut v = vec![];
                    for a_ind in &b.attackers {
                        let a = &self.arguments[*a_ind];
                        v.push(format!("{} -> {}", a, b));
                    }
                    v
                })
                .collect::<Vec<_>>()
                .join("\n"),
        )
    }
}
