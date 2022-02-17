use super::AF;
use sat_portfolio::solver::Model;
use std::fmt;

pub struct Extension<'a> {
    af: &'a AF,
    model: &'a Model,
}

impl<'a> Extension<'a> {
    pub fn new(af: &'a AF, model: &'a Model) -> Self {
        Self { af, model }
    }
}

impl fmt::Display for Extension<'_> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            write!(f, "[{}]", self
                .model
                .get_pos_vars()
                .iter()
                .filter_map(|var| self.af.get_arg(&var))
                .map(|l| format!("{}", l))
                .collect::<Vec<_>>()
                .join(",")
            )
    }
}
