See the [Scientific Python Developer Guide][spc-dev-intro] for a detailed description of best practices for developing scientific packages.

[spc-dev-intro]: https://learn.scientific-python.org/development/

# Setting up a development environment

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and virtual environments.

```bash
uv sync --extra dev
```

Then install the pre-commit hook so the gates run before each commit:

```bash
uv run pre-commit install
```

# Quality gates

Every rule this project adopts has a gate that enforces it. A rule that exists only as prose erodes silently, so each one below fails the build rather than relying on review.

| Gate | Enforces | Runs in |
|---|---|---|
| ruff check | Lint rules configured in `pyproject.toml` | pre-commit, CI |
| ruff format | Consistent formatting | pre-commit, CI |
| mypy | Type annotations on `src/` and `examples/` | pre-commit, CI |
| vulture | No unused functions, methods, or attributes | pre-commit, CI |
| pytest | Every pattern has passing tests | CI |
| Coverage | Line coverage stays at or above 97% | CI, `make check` |
| Module length | No module exceeds 1000 lines | pytest (`tests/test_module_length_gate.py`) |
| mkdocs --strict | Documentation builds with no warnings | CI |

Vulture runs at 60% confidence, the level at which it reports unused functions, methods, and attributes. A higher threshold catches only unused imports, which ruff already covers, and would make the gate decorative.

Run them all locally with:

```bash
make check
```

Or individually: `make lint`, `make typecheck`, `make deadcode`, `make coverage`, `make docs-build`. Use `make test` for a fast run without the coverage threshold.

## The coverage threshold

`fail_under` in `pyproject.toml` records the coverage measured on the day it was adopted (97% on 260812). It is a ratchet: raise it when coverage improves, never lower it to make a change pass.

## The module length gate

`tests/test_module_length_gate.py` enforces the 1000-line cap using the `GrandfatheredLimit` class from this catalog's own gate patterns. It applies three checks: a new module over the cap fails, a module recorded as existing debt may shrink but never grow, and a recorded entry that now passes the cap must be deleted. The `GRANDFATHERED` mapping is empty today because no module exceeds the cap; add an entry only when adopting a stricter rule that existing code cannot meet at once.

# Testing

```bash
make test              # run the suite
make coverage          # run with a coverage report
```

Tests use pytest. Write the test before the implementation and confirm it fails against the unfixed code first: a test that passes on broken code is worse than none.

# Documentation

```bash
make docs              # serve locally with hot reload
make docs-build        # build with --strict, as CI does
```

Documentation lives under `docs/` and is built with mkdocs. Every pattern page follows the same structure: Overview, Usage Guidelines, Implementation, Trade-offs, Real-World Examples, Related Patterns, and an API Reference block that pulls docstrings from the module.

# Adding a pattern

1. Write the documentation page under `docs/patterns/<category>/` and add it to the `nav` in `mkdocs.yml` and the table in `docs/overview.md`.
2. Write the tests under `tests/` and confirm they fail.
3. Implement the module under `src/design_patterns/<category>/`.
4. Run `make check`.
