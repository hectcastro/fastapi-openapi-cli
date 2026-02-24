# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A CLI tool that exports OpenAPI specifications from FastAPI applications to JSON or YAML formats. Built with modern Python tooling emphasizing strict type safety and 100% test coverage.

## Commands

### Development Setup

```bash
# Install dependencies (includes dev dependencies)
uv sync
```

### Testing

```bash
# Run all tests with coverage (100% coverage required)
make test

# Run specific test file
uv run pytest tests/test_cli.py

# Run single test function
uv run pytest tests/test_cli.py::test_function_name

# Run without coverage
uv run pytest --no-cov
```

### Code Quality

```bash
# Run all checks (lint, types, tests) - same as CI
make ci

# Individual checks
make lint     # Lint with ruff
make format   # Format code with ruff
make types    # Type check with ty
make deps     # Check dependencies with deptry
```

### Running the CLI in Development

```bash
# Run locally with test fixture
uv run fastapi-openapi --app tests.fixtures.sample_app:app

# Run with output to file
uv run fastapi-openapi --app tests.fixtures.sample_app:app -o openapi.json
```

## Architecture

### Core Components

The codebase follows a three-layer architecture:

1. **CLI Layer** (`cli.py`): argparse-based command-line interface that orchestrates the workflow
2. **Loader Layer** (`loader.py`): Dynamically imports and validates FastAPI applications from module paths
3. **Export Layer** (`export.py`): Extracts OpenAPI specs and serializes to JSON/YAML

### Key Design Patterns

**App Path Format**: The tool accepts FastAPI applications using the `module:attribute` format (e.g., `myapp.main:app`). The loader splits this string, imports the module, retrieves the attribute, and validates it's a FastAPI instance.

**Format Detection**: Output format is determined by file extension (`.json`, `.yaml`, `.yml`). If no output path is provided, defaults to JSON on stdout.

**Error Handling**: Custom `AppLoadError` exception provides clear error messages for common issues:
- Module not found
- Attribute doesn't exist
- Attribute is not a FastAPI instance

### Test Structure

Tests are organized by component (not 1:1 with source files) and focus on behavior:
- `test_cli.py`: End-to-end CLI behavior including error cases
- `test_export.py`: OpenAPI extraction and serialization behavior
- `test_loader.py`: App loading validation and error handling
- `tests/fixtures/`: Sample FastAPI apps for testing different scenarios

**Testing CLI output**: The test suite invokes `main(argv)` directly and uses `capsys` to assert stdout/stderr behavior for help, success, and error paths.

## Code Standards

### Dependency Management

- Uses **dependency-groups** (PEP 735) instead of optional-dependencies for dev tools
- `pyproject.toml` is the single source of truth for package version

### Type Safety

- Python 3.12+ with strict type checking via `ty`
- All function signatures must include type annotations
- No `Any` types or type: ignore comments

### Test Coverage

- 100% coverage is enforced (`--cov-fail-under=100`)
- Tests must verify behavior, not implementation details
- Coverage configuration excludes `if TYPE_CHECKING:` blocks

### Code Style

- Line length: 100 characters
- Ruff linting with strict rules enabled (pycodestyle, pyflakes, isort, pep8-naming, etc.)
- Follow functional programming patterns where appropriate

## CLI Entry Point

The package uses `[project.scripts]` in `pyproject.toml` to create the `fastapi-openapi` console script:
```toml
[project.scripts]
fastapi-openapi = "fastapi_openapi_cli.cli:main"
```
This points to the `main` function in `cli.py`, which parses CLI arguments and returns process exit codes.

## Release Process

**Quick Summary:**
1. Update version in `pyproject.toml`
2. Create and push a git tag (e.g., `v0.2.0`)
3. Create a GitHub release from the tag
4. GitHub Actions automatically builds and publishes to PyPI using trusted publishing (OIDC)

**First-time setup:** Configure PyPI trusted publisher at https://pypi.org/manage/account/publishing/ with the repository details.
