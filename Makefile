EXECUTOR := uv run

.PHONY: all

test:
	$(EXECUTOR) pytest

pc: pre-commit
pre-commit:
	$(EXECUTOR) pre-commit run --all-files

lint:
	$(EXECUTOR) ruff check

format:
	$(EXECUTOR) ruff format --check

lx: lint-fix
lint-fix:
	$(EXECUTOR) ruff check --fix

fx: format-fix
format-fix:
	$(EXECUTOR) ruff format
