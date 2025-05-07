# Python Base

## Overview

A starter repository for Python projects, following best practices and conventions. It provides tools and libraries to help you get started quickly.

## Project Structure

Modules in the `src` directory are organized into two main categories:

- **Applications**: Main entry points (e.g., CLI, API). Executed directly.
- **Libraries**: Reusable components. Imported by applications, not executed directly. (e.g., `src/lib_core`)

## Features

### Logging Configuration

Logging adapts to the environment:

- **Development**: Human-friendly formatting (colors, indentation), level set to `DEBUG` (all logs shown).
- **Production**: Machine-friendly, single-line JSON logs, level set to `INFO` (only info and above).

| Development | Production |
| ----------- | ---------- |
| ![Development Log Example](docs/assets/logs_dev.png) | ![Production Log Example](docs/assets/logs_prod.png) |

**Usage Example:**

```python
from logging import get_logger

logger = get_logger(__name__)
logger.debug("This is a debug message")
```

### Application Settings Management

Settings are managed with [pydantic-settings](https://pydantic-docs.helpmanual.io/usage/settings.html), loaded from environment variables or a `.env` file.

- Base settings class: `src/core/settings/`
- Each app extends this class and defines its own settings.

**Defining Settings:**

```python
from functools import lru_cache
from lib_core.settings import AppBaseSettings

class Settings(AppBaseSettings):
    pass

@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type: ignore
```

- Libraries can define specialized settings (e.g., `LogsSettings`).
- Applications using a library should include its settings in their own settings class.

**Example:**

```python
from lib_core.settings import AppBaseSettings
from lib_genai import GenAISettings

class Settings(AppBaseSettings):
    genai: GenAISettings = GenAISettings()
```

**Using Settings:**

- Import and call `get_settings()` to access settings.
- For testability, pass settings as parameters to functions instead of relying on singletons.

```python
from app.settings import get_settings, Settings

def main(*, settings: Settings = get_settings()) -> None:
    pass
```

- This approach is also useful for libraries used in multiple apps or with different settings.

```python
# In the library
from lib_bigquery import BigQueryTableSettings

def count_rows(bigquery_table: BigQueryTableSettings) -> int:
    ...

# In the application
from lib_core.settings import AppBaseSettings
from lib_bigquery import BigQueryTableSettings

class Settings(AppBaseSettings):
    input_bigquery: BigQueryTableSettings = BigQueryTableSettings()
    output_bigquery: BigQueryTableSettings = BigQueryTableSettings()

def main(*, settings: Settings = get_settings()) -> None:
   output_row_count = count_rows(bigquery_table=settings.output_bigquery)
```

## Development

### Install Dependencies

```bash
uv sync --all-groups --all-extras
```

#### Pre-commit Hooks

- Install pre-commit hooks:

```bash
pre-commit install
```
- Run pre-commit hooks manually:

```bash
make pre-commit # or, the alias
make pc
```

### Running the Application

#### Standalone Project

- Ensure a script is defined in `pyproject.toml`:

```toml
[project.scripts]
app = "app.main:main"
```

- Run:

```bash
uv run app
```

#### Module Project

- Run as a module (e.g., FastAPI):

```bash
uv run fastapi dev src/api
```

### Development Commands

A `Makefile` is provided for common tasks. See the file for details.

- **Run tests:**
  ```bash
  make test
  ```
- **Run linter:**
  ```bash
  make lint      # Check
  make lint-fix   # Autofix
  make lx        # Autofix Alias
  ```
- **Run formatter:**
  ```bash
  make format      # Check
  make format-fix   # Autofix
  make fx          # Autofix Alias
  ```

---

## Build

A [Dockerfile](./Dockerfile) is provided for building the project.

- Uses a multi-stage build: dependencies and project installed in a builder image, then copied to a smaller final image.
- The final image contains only the necessary files.
- Each application can extend the base image and define its own entrypoint/environment.

**Build the image:**

```bash
docker build \
    --target app \
    -t <image-name> \
    .
```
