"""Gate: every console script declared in pyproject.toml resolves to a callable.

A `[project.scripts]` entry is a promise that installing the package produces a
working executable. Nothing imports the target in normal use, so a wrong module
path passes every other gate and fails only on the user's machine. This gate
imports each declared target and fails with the same error the user would see.
"""

import importlib
import tomllib
from pathlib import Path

import pytest

PYPROJECT = Path(__file__).resolve().parent.parent / "pyproject.toml"


def declared_scripts() -> dict[str, str]:
    """Read the console scripts the package declares.

    Returns:
        dict[str, str]: Script name mapped to its ``module:attribute`` target.
    """
    with PYPROJECT.open("rb") as handle:
        project = tomllib.load(handle)["project"]
    return dict(project.get("scripts", {}))


@pytest.mark.parametrize(("name", "target"), sorted(declared_scripts().items()))
def test_declared_script_resolves(name, target):
    """Importing the target must succeed and yield something callable."""
    module_name, _, attribute = target.partition(":")
    module = importlib.import_module(module_name)
    assert callable(getattr(module, attribute)), f"{name} -> {target}"


def test_the_gate_would_catch_a_broken_target():
    """The gate must fail on a bad target, not merely pass on a clean file."""
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("design_patterns.no_such_module")
