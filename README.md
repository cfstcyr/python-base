# Python base

## Develop

### Install dependencies

```bash
uv sync --all-groups --all-extras
```

### Run the application

Running the application depends on the project.

#### Run a standalone project

A standalone project is a project that is executed directly (e.g. `python main.py`).

To do so, you must make sure that a script is defined in the `pyproject.toml` file.

For example, to run that `main` function in the `src/app/main.py` file, you must have the following in your `pyproject.toml` file:

```toml
[project.scripts]
app = "app.main:main"
```

Then, you can run the application with:

```bash
uv run app
```

#### Run a module

A module is a project that is executed as a module (e.g. `fastapi dev src/api`).

You can run the module with:

```bash
uv run fastapi dev src/api
```

### Run tests

```bash
# Makefile command
make test

# uv command
uv run pytest
```

### Run linter

```bash
# Makefile command
make lint
# Makefile command with autofix
make lint-fix
make lx

# uv command
uv run ruff check
# uv command with autofix
uv run ruff check --fix
```

### Run formatter

```bash
# Makefile command
make format
# Makefile command with autofix
make format-fix
make fx

# uv command
uv run ruff format --check
# uv command with autofix
uv run ruff format
```

## Build

A [Dockerfile](./Dockerfile) is provided to build the project.

The Dockerfile works by installing the dependencies and the project in a virtual environment in a builder image. Then, it copies the virtual environment to a new image and runs the application.

When looking at the Dockerfile, you will see that the content of this repository is not copied to the final image. This is because the Dockerfile uses a multi-stage build, which allows you to copy only the necessary files from the builder image to the final image.

This way, the final image is smaller and only contains the dependencies and the project.

Then, each application extends the base image and defines its own entrypoint and or environment.

### Build the image

```bash
docker build \
    --target app \
    -t <image-name> \
    .
```
