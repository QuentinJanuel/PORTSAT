mod argument;
mod attack;

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
    pub fn from(args: Vec<&str>, attacks: Vec<(&str, &str)>) -> Self {
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
