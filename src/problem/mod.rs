mod semantics;
mod task;

use crate::af::Argument;
use std::{
    fmt,
    convert::From,
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

impl From<(&str, Option<&str>)> for Problem {
    fn from((input, arg): (&str, Option<&str>)) -> Self {
        let mut parts = input.split("-");
        let task = parts
            .next()
            .ok_or(())
            .map(|task| (task, arg).into())
            .expect("Invalid task");
        let semantics = parts
            .next()
            .expect("")
            .parse()
            .expect("Invalid semantics");
        Self {
            task,
            semantics,
        }
    }
}


pub fn all_problems() {
    let all_tasks = vec![
        Task::Credulous(Argument(String::new())),
        Task::Skeptical(Argument(String::new())),
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
