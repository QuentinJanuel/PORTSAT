use std::{
    fmt,
    str::FromStr,
};

pub enum Format {
    TGF,
    APX,
    LooseAPX,
    PAF,
}

impl Format {
    pub fn show_available() {
        println!("[{}]", [
            // Format::TGF,
            // Format::APX,
            // Format::LooseAPX,
            Format::PAF,
        ]
            .iter()
            .map(|f| f.to_string())
            .collect::<Vec<_>>()
            .join(","));
    }
}

impl fmt::Display for Format {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Format::TGF => write!(f, "tgf"),
            Format::APX => write!(f, "apx"),
            Format::LooseAPX => write!(f, "loose-apx"),
            Format::PAF => write!(f, "paf"),
        }
    }
}

impl FromStr for Format {
    type Err = String;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "tgf" => Ok(Format::TGF),
            "apx" => Ok(Format::APX),
            "loose-apx" => Ok(Format::LooseAPX),
            "paf" => Ok(Format::PAF),
            _ => Err(format!("Unknown format: {}", s)),
        }
    }
}
