mod semantics;
mod task;

use std::{
    fmt,
    str::FromStr,
};
pub use semantics::Semantics;
pub use task::Task;

pub struct Problem {
    pub task: Task,
    pub semantics: Semantics,
}

impl fmt::Display for Problem {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}-{}", self.task, self.semantics)
    }
}

impl FromStr for Problem {
    type Err = ();
    fn from_str(input: &str) -> Result<Self, Self::Err> {
        let mut parts = input.split("-");
        let task = parts.next().ok_or(())?.parse()?;
        let semantics = parts.next().ok_or(())?.parse()?;
        Ok(Self {
            task,
            semantics,
        })
    }
}


pub fn all_problems() {
    let all_tasks = vec![
        Task::Credulous,
        Task::Skeptical,
        Task::Enumerate,
        Task::FindOne,
    ];
    let all_semantics = vec![
        Semantics::Complete,
        Semantics::Grounded,
        Semantics::Preferred,
        Semantics::Stable,
    ];
    let all_problems = all_tasks
        .iter()
        .flat_map(|task| {
            all_semantics
                .iter()
                .map(move |semantics| Problem {
                    task: task.clone(),
                    semantics: semantics.clone(),
                })
        })
        .collect::<Vec<_>>();
    println!(
        "[{}]",
        all_problems
            .iter()
            .map(Problem::to_string)
            .collect::<Vec<_>>()
            .join(","),
    );
}
