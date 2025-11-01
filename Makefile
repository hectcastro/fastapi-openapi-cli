.PHONY: test types lint format ci deps

test:
	uv run pytest

types:
	uv run ty check src tests

lint:
	uv run ruff check .

format:
	uv run ruff format .

ci: lint types test

deps:
	uv run deptry .
