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

## Solve a given problem
```
cargo run -- -p <problem> -f <file> -fo <fileformat> [-a <additional_parameter>]
```
Example:
```
cargo run -- -p DC-CO -f examples/tgf.txt -fo tgf -a a
```

## Compile
```
cargo build --release
```