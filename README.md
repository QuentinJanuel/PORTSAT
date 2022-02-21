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
cargo run -- -p <problem> -s <solvers> -f <file> -fo <fileformat> [-a <additional_parameter>]
```
Example:
```
cargo run -- -p DC-CO -s manysat,dpll -f examples/tgf.txt -fo tgf -a a
```

## Compile
```
cargo build --release
```