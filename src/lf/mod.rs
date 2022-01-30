// Logical Formula
#[derive(Debug)]
pub enum LF {
    Atom(String),
    Not(Box<LF>),
    And(Box<LF>, Box<LF>),
    Or(Box<LF>, Box<LF>),
}
