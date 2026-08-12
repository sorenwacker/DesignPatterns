.PHONY: help install check lint format typecheck deadcode test coverage docs docs-build hooks clean

help:
	@echo "install     install the project and dev dependencies"
	@echo "hooks       install the pre-commit hook"
	@echo "check       run every quality gate"
	@echo "lint        ruff check"
	@echo "format      ruff format"
	@echo "typecheck   mypy on src and examples"
	@echo "deadcode    vulture"
	@echo "test        pytest"
	@echo "coverage    pytest with a coverage report"
	@echo "docs        serve the documentation with hot reload"
	@echo "docs-build  build the documentation with --strict, as CI does"

install:
	uv sync --extra dev

hooks:
	uv run pre-commit install

check: lint typecheck deadcode coverage docs-build

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .
	uv run ruff check --fix .

typecheck:
	uv run mypy src examples

deadcode:
	uv run vulture

test:
	uv run pytest

coverage:
	uv run pytest --cov=design_patterns --cov-report=term-missing

docs:
	uv run mkdocs serve

docs-build:
	uv run mkdocs build --strict

clean:
	rm -rf site htmlcov .pytest_cache .mypy_cache .coverage
