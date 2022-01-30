mod lf;
mod af;
mod utils;
mod problem;

use af::AF;
use problem::Problem;
use utils::args::Args;

fn main() {
    let args = Args::new();
    if args.has("--problems") {
        problem::all_problems();
    } else if args.has("--formats") {
        println!("[tgf]");
    } else if let Some(problem) = args.get("-p") {
        let problem = problem.parse::<Problem>()
            .expect("Invalid problem");
        let file = args.get("-f")
            .expect("The file is not specified");
        let param = args.get("-a").unwrap_or("");
        let tgf = utils::read_file(file);
        let af = AF::from_tgf(&tgf);
        let lf = af.phi(&problem.semantics);
        println!("Problem: {}", problem);
        println!("Additional param: {}", param);
        println!("AF:\n{}", af);
        println!("LF:\n{:?}", lf);
    } else {
        utils::details();
    }
}
