EXECUTOR := uv run python

.PHONY: all

lint:
	$(EXECUTOR) -m ruff check

format:
	$(EXECUTOR) -m ruff format --check

lx: lint-fix
lint-fix:
	$(EXECUTOR) -m ruff check --fix

fx: format-fix
format-fix:
	$(EXECUTOR) -m ruff format