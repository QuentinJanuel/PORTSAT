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
    fn get_args(&'a self) -> Vec<&'a str>{
        self.model
            .get_pos_vars()
            .iter()
            .filter_map(|var|
                self.af
                    .arguments
                    .get(var.0 as usize)
                    .map(|arg| arg.name.as_str())
            )
            .collect()
    }
    pub fn contains(&self, arg: &str) -> bool {
        self.get_args().contains(&arg)
    }
    pub fn is_subset(&self, other: &Self) -> bool {
        self.get_args().iter().all(|arg| other.contains(arg))
    }
}

impl fmt::Display for Extension<'_> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "w {}", self.get_args().join(" "))
    }
}
