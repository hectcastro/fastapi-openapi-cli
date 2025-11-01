# fastapi-openapi-cli

A command-line tool to export OpenAPI specifications from FastAPI applications.

## Installation

```bash
uv add fastapi-openapi-cli
```

## Usage

### Basic Usage

Export OpenAPI spec to `stdout`:

```bash
fastapi-openapi --app myapp.main:app
```

Export to JSON File:

```bash
fastapi-openapi --app myapp.main:app -o openapi.json
```

Export to YAML File:

```bash
fastapi-openapi --app myapp.main:app -o openapi.yaml
```

## Development

### Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management:

```bash
# Clone the repository
git clone https://github.com/hectcastro/fastapi-openapi-cli.git
cd fastapi-openapi-cli

# Install dependencies
uv sync --all-extras
```

### Running Tests

```bash
# Run all tests with coverage
uv run pytest

# Run specific test file
uv run pytest tests/test_cli.py

# Run without coverage
uv run pytest --no-cov
```

### Linting and Formatting

```bash
# Check code with ruff
uv run ruff check .

# Fix issues automatically
uv run ruff check --fix .

# Format code
uv run ruff format .
```

### Type Checking

```bash
# Run type checking with ty
uv run ty check src
```

### Running the CLI Locally

```bash
# Run the CLI in development
uv run fastapi-openapi --app tests.fixtures.sample_app:app
```
