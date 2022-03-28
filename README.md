# Computational model of argumentation

You can use the solver as described in the ICCMA'15 Supplementary Notes on probo:

## Print the name, version and authors
```
cargo run --
```

## Print the supported formats
```
cargo run -- --formats
```
**NOTE:** We have an extra format `loose-apx` which allows for APX file with less assumptions (e.g. the arguments and attacks can be mixed, or there can be multiple definitions per line). If your APX graph fails to parse with the default `apx` format, give a try to `loose-apx`. However the parsing is slower.

## Print the supported problems
```
cargo run -- --problems
```

## Print the available SAT solvers
```
cargo run -- --solvers
```

## Solve a given problem
```
cargo run -- -p <problem> -f <file> -fo <fileformat> [-a <additional_parameter>] [-s <solvers>]
```
Example:
```
cargo run -- -p DC-CO -s manysat,dpll -f graph.tgf -fo tgf -a a
```
**NOTE**: You cannot set the solvers when the problem involves the grounded extension.

## Prerequisite
 - [Rust](https://www.rust-lang.org/)
 - [Python](https://www.python.org/) (10.0 or higher)
### MacOS
Make sure to have the `libomp` library installed. If you don't, you can install it with the following command:
```bash
brew install libomp
```

## Compile
The Python scripts will attempt to use the release version of the solver.
In order to compile it, run the following command:
```
cargo build --release
```
In order to install the python dependencies, run
```
pip install -r requirements.txt
```