pub mod args;

use std::{
    fs::File,
    io::Read,
};

pub fn read_file(path: &str) -> String {
    let mut file = File::open(path).unwrap();
    let mut contents = String::new();
    file.read_to_string(&mut contents).unwrap();
    contents
}

pub fn details() {
    let name = env!("CARGO_PKG_NAME");
    let version = env!("CARGO_PKG_VERSION");
    let author = env!("CARGO_PKG_AUTHORS")
        .split(":")
        .collect::<Vec<_>>()
        .join(", ");
    println!("{} v{}\n{}", name, version, author);
}
