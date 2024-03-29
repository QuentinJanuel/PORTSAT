mod semantics;
mod task;

use std::{
    fmt,
    convert::TryFrom,
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

impl TryFrom<(&str, Option<&str>)> for Problem {
    type Error = &'static str;
    fn try_from((input, arg): (&str, Option<&str>)) -> Result<Self, Self::Error> {
        let mut parts = input.split("-");
        let task = parts
            .next()
            .ok_or("The task is not specified")?;
        let task = Task::try_from((task, arg))?;
        let semantics = parts
            .next()
            .ok_or("The semantics is not specified")?;
        let semantics = Semantics::try_from(semantics)?;
        Ok(Self {
            task,
            semantics,
        })
    }
}


pub fn all_problems() {
    let all_tasks = vec![
        Task::Credulous(String::new()),
        Task::Skeptical(String::new()),
        // Task::Enumerate,
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
