"""Gates for the runnable examples.

The examples are consumers of the library. Three rules keep them that way and
keep their index honest: an example must not redefine a class the library
already provides, every example the README lists must exist and every example
must be listed, and every example must run to completion.
"""

import ast
import re
import runpy
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = REPOSITORY_ROOT / "examples"
LIBRARY = REPOSITORY_ROOT / "src" / "design_patterns"
EXAMPLE_SCRIPTS = sorted(EXAMPLES.glob("*.py"))


def defined_classes(path: Path) -> set[str]:
    """Names of the classes a module defines at any nesting level.

    Args:
        path: Python source file.

    Returns:
        set[str]: Class names found by parsing the file.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}


@pytest.fixture(scope="module")
def library_classes() -> set[str]:
    """Every class name the library defines."""
    return set().union(*(defined_classes(p) for p in LIBRARY.rglob("*.py")))


@pytest.mark.parametrize("script", EXAMPLE_SCRIPTS, ids=lambda p: p.name)
def test_example_does_not_redefine_a_library_class(script, library_classes):
    """A copy of a library class silently diverges; the example must import it."""
    forked = defined_classes(script) & library_classes
    assert not forked, f"{script.name} redefines {sorted(forked)}; import instead"


def listed_examples() -> set[str]:
    """Example file names the examples README claims exist."""
    readme = (EXAMPLES / "README.md").read_text(encoding="utf-8")
    return set(re.findall(r"`([a-z_]+\.py)`", readme))


def test_every_listed_example_exists():
    """The README must not advertise scripts that are not in the tree."""
    missing = listed_examples() - {p.name for p in EXAMPLE_SCRIPTS}
    assert not missing, sorted(missing)


def test_every_example_is_listed():
    """A script the README does not mention is invisible to readers."""
    unlisted = {p.name for p in EXAMPLE_SCRIPTS} - listed_examples()
    assert not unlisted, sorted(unlisted)


@pytest.mark.parametrize("script", EXAMPLE_SCRIPTS, ids=lambda p: p.name)
def test_example_runs_to_completion(script, capsys):
    """Each example runs as a script and reports the benefits it demonstrates."""
    runpy.run_path(str(script), run_name="__main__")
    assert "Benefits of" in capsys.readouterr().out


def test_the_gates_cover_the_examples():
    """Gates over an empty directory prove nothing."""
    assert len(EXAMPLE_SCRIPTS) >= 5
