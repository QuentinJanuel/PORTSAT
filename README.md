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

## Compile
The Python scripts will attempt to use the release version of the solver.
In order to compile it, run the following command:
```
cargo build --release
```