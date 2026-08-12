"""Gate: no module in this repository exceeds the length cap.

The rule is that no file should exceed 1000 lines. Stated only in prose it would
erode one reasonable-looking addition at a time, so it is enforced here using the
GrandfatheredLimit pattern from this catalog.

The three checks are deliberate. A new module over the cap fails outright. A
module recorded as existing debt may shrink but never grow. And a recorded entry
that now passes the cap must be deleted, which is the check that keeps the list
honest: after a module is split, a forgotten entry makes the debt look worse than
it is, and a list known to be wrong stops being read.
"""

from pathlib import Path

import pytest

from design_patterns.gates.grandfathered_debt import GrandfatheredLimit

CAP = 1000

#: Module -> its length when this gate was added (260812). Lower a number when
#: the module shrinks; delete the entry when it passes the cap. The mapping is
#: empty because no module exceeded the cap on adoption, and it should stay that
#: way: entries are for adopting a rule existing code cannot yet meet.
GRANDFATHERED: dict[str, int] = {}

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
CHECKED_DIRECTORIES = ("src", "tests", "examples")

LIMIT = GrandfatheredLimit(cap=CAP, recorded=GRANDFATHERED, recorded_on="260812")


def measure_module_lengths() -> dict[str, int]:
    """Count the lines of every Python module under the checked directories.

    Returns:
        dict[str, int]: Repository-relative module path mapped to its line count.
    """
    return {
        str(path.relative_to(REPOSITORY_ROOT)): len(
            path.read_text(encoding="utf-8").splitlines()
        )
        for directory in CHECKED_DIRECTORIES
        for path in sorted((REPOSITORY_ROOT / directory).rglob("*.py"))
    }


@pytest.fixture(scope="module")
def lengths():
    """Line counts for every module the gate covers."""
    return measure_module_lengths()


def test_the_gate_covers_the_repository(lengths):
    """A gate measuring nothing would pass silently and prove nothing."""
    assert len(lengths) > 50


def test_no_new_module_exceeds_the_cap(lengths):
    """A module written after adoption must meet the cap in full."""
    violations = LIMIT.new_violations(lengths)
    assert not violations, "\n".join(violations)


def test_no_recorded_module_has_grown(lengths):
    """Recorded debt may shrink, never grow."""
    violations = LIMIT.worsened(lengths)
    assert not violations, "\n".join(violations)


def test_the_allow_list_holds_no_module_that_passes(lengths):
    """A stale entry makes the debt look worse than it is."""
    violations = LIMIT.stale_entries(lengths)
    assert not violations, "\n".join(violations)


def test_the_cap_would_catch_an_oversized_module(lengths):
    """The gate must fail on a violation, not merely pass on a clean tree.

    Written because a gate proven only against compliant input demonstrates
    nothing about whether it can fail at all.
    """
    oversized = dict(lengths)
    oversized["src/design_patterns/invented_module.py"] = CAP + 1
    violations = GrandfatheredLimit(
        cap=CAP, recorded=GRANDFATHERED, recorded_on="260812"
    ).new_violations(oversized)
    assert len(violations) == 1
    assert "invented_module.py" in violations[0]
