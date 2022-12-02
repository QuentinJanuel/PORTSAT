NAME = portsat

build:
	cargo build --release
	cp target/release/$(NAME) $(NAME)