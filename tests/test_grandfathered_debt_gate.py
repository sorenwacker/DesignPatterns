"""Tests for the Grandfathered-Debt Gate pattern."""

import pytest

from design_patterns.gates.grandfathered_debt import GrandfatheredLimit

CAP = 666
RECORDED = {"pkg/metadata_definitions.py": 1191, "pkg/importer/isa.py": 842}


@pytest.fixture
def limit():
    """A module length cap adopted against an already-violating codebase."""
    return GrandfatheredLimit(cap=CAP, recorded=RECORDED, recorded_on="260806")


class TestNewViolations:
    """Modules over the cap that were never recorded."""

    def test_a_new_module_over_the_cap_fails(self, limit):
        """The rule applies in full to anything written after adoption."""
        (message,) = limit.new_violations({"pkg/report.py": 700})
        assert "pkg/report.py" in message

    def test_a_new_module_under_the_cap_passes(self, limit):
        """Compliant new code produces no message."""
        assert limit.new_violations({"pkg/report.py": 400}) == []

    def test_a_module_exactly_at_the_cap_passes(self, limit):
        """The cap is a limit, not an exclusive bound."""
        assert limit.new_violations({"pkg/report.py": CAP}) == []

    def test_a_recorded_module_is_not_a_new_violation(self, limit):
        """Existing debt is tolerated by this check and caught by the next."""
        assert limit.new_violations({"pkg/importer/isa.py": 842}) == []

    def test_the_message_says_the_list_is_closed(self, limit):
        """New entries must not be added to the allow list."""
        (message,) = limit.new_violations({"pkg/report.py": 700})
        assert "the allow list is closed" in message


class TestWorsenedDebt:
    """Recorded modules that have grown."""

    def test_growth_of_recorded_debt_fails(self, limit):
        """Recorded debt may shrink but never grow."""
        (message,) = limit.worsened({"pkg/importer/isa.py": 900})
        assert "pkg/importer/isa.py" in message

    def test_shrinking_recorded_debt_passes(self, limit):
        """Progress is permitted without editing the gate first."""
        assert limit.worsened({"pkg/importer/isa.py": 800}) == []

    def test_an_unchanged_measurement_passes(self, limit):
        """Standing still is tolerated; the ratchet only blocks regression."""
        assert limit.worsened({"pkg/importer/isa.py": 842}) == []

    def test_the_message_carries_the_recorded_value_and_date(self, limit):
        """A measured fact with a date stays checkable as the code changes."""
        (message,) = limit.worsened({"pkg/importer/isa.py": 900})
        assert "842" in message
        assert "260806" in message
        assert "900" in message


class TestStaleEntries:
    """Recorded modules that now pass the cap."""

    def test_an_entry_that_now_passes_fails(self, limit):
        """The check most often left out is the one that keeps the list honest."""
        (message,) = limit.stale_entries({"pkg/importer/isa.py": 300})
        assert "pkg/importer/isa.py" in message

    def test_an_entry_still_over_the_cap_is_not_stale(self, limit):
        """Outstanding debt is not a stale entry."""
        assert limit.stale_entries({"pkg/importer/isa.py": 800}) == []

    def test_an_unmeasured_entry_is_not_reported(self, limit):
        """A module absent from the measurements says nothing about the entry."""
        assert limit.stale_entries({"pkg/report.py": 100}) == []

    def test_the_message_asks_for_the_entry_to_be_deleted(self, limit):
        """After a split, a forgotten entry makes the debt look worse than it is."""
        (message,) = limit.stale_entries({"pkg/importer/isa.py": 300})
        assert "Delete its entry" in message


class TestCombinedViolations:
    """All three checks reported together."""

    def test_a_compliant_measurement_produces_nothing(self, limit):
        """Unchanged debt and compliant new code pass every check."""
        assert limit.violations({**RECORDED, "pkg/report.py": 100}) == []

    def test_all_three_failures_are_reported_at_once(self, limit):
        """The three failures call for three different responses."""
        violations = limit.violations(
            {
                "pkg/report.py": 700,  # new violation
                "pkg/metadata_definitions.py": 1300,  # worsened
                "pkg/importer/isa.py": 300,  # stale entry
            }
        )
        assert len(violations) == 3

    def test_check_raises_when_any_check_fails(self, limit):
        """check is the assertion form of violations."""
        with pytest.raises(AssertionError, match="pkg/report.py"):
            limit.check({**RECORDED, "pkg/report.py": 700})

    def test_check_passes_on_a_compliant_codebase(self, limit):
        """A codebase within the ratchet passes quietly."""
        limit.check(RECORDED)
