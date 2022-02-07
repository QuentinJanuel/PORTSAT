pub struct Args {
    args: Vec<String>,
}

impl Args {
    pub fn new() -> Self {
        Self {
            args: std::env::args()
                .skip(1)
                .collect::<Vec<_>>(),
        }
    }
    pub fn has(&self, arg: &str) -> bool {
        self.args.contains(&arg.to_string())
    }
    pub fn get(&self, arg: &str) -> Option<&str> {
        let pos = self
            .args
            .iter()
            .position(|a| a == arg);
        pos
            .and_then(|i| self.args.get(i + 1))
            .map(String::as_str)
    }
}
