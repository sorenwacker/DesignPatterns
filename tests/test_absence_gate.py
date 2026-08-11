"""Tests for the Absence Gate pattern."""

import types

import pytest

from design_patterns.gates.absence import AbsenceGate, WithdrawnName

IMPORTED_SUFFIX = WithdrawnName(
    name="IMPORTED_SUFFIX",
    withdrawn_on="260806",
    reason=(
        "The suffix described how a record reached the system rather than what "
        "it was, and deriving it from a mutable field broke every re-import "
        "after a rename."
    ),
)


class TestWithdrawnName:
    """Tests for the WithdrawnName record."""

    def test_message_names_the_withdrawn_name(self):
        """The failure text identifies which name came back."""
        assert "IMPORTED_SUFFIX" in IMPORTED_SUFFIX.message()

    def test_message_carries_the_date_and_the_reason(self):
        """The date and the original failure are the payload of the gate."""
        message = IMPORTED_SUFFIX.message()
        assert "260806" in message
        assert "broke every re-import after a rename" in message

    def test_the_record_is_immutable(self):
        """A recorded decision must not be edited in place by a caller."""
        with pytest.raises(AttributeError):
            IMPORTED_SUFFIX.name = "OTHER"  # type: ignore[misc]


class TestAbsenceGate:
    """Tests for AbsenceGate."""

    def test_absent_name_produces_no_violation(self):
        """A namespace without the withdrawn name passes."""
        namespace = types.SimpleNamespace(build_identifier=str)
        assert AbsenceGate([IMPORTED_SUFFIX]).violations(namespace) == []

    def test_reintroduced_name_produces_a_violation(self):
        """The gate detects the withdrawn name being defined again."""
        namespace = types.SimpleNamespace(IMPORTED_SUFFIX=" (imported)")
        violations = AbsenceGate([IMPORTED_SUFFIX]).violations(namespace)
        assert len(violations) == 1
        assert "IMPORTED_SUFFIX" in violations[0]

    def test_violation_message_says_what_to_do(self):
        """A bare assertion is worthless; the message must instruct."""
        namespace = types.SimpleNamespace(IMPORTED_SUFFIX=" (imported)")
        (message,) = AbsenceGate([IMPORTED_SUFFIX]).violations(namespace)
        assert "Remove it again" in message

    def test_every_reintroduced_name_is_reported(self):
        """One run reports all reintroductions, not only the first."""
        other = WithdrawnName(
            name="LEGACY_MODE", withdrawn_on="260701", reason="It had no callers."
        )
        namespace = types.SimpleNamespace(IMPORTED_SUFFIX="x", LEGACY_MODE=True)
        violations = AbsenceGate([IMPORTED_SUFFIX, other]).violations(namespace)
        assert len(violations) == 2

    def test_check_passes_when_the_name_is_gone(self):
        """check returns quietly when nothing was reintroduced."""
        AbsenceGate([IMPORTED_SUFFIX]).check(types.SimpleNamespace())

    def test_check_raises_with_the_recorded_reason(self):
        """check fails loudly, carrying the reason into the test report."""
        namespace = types.SimpleNamespace(IMPORTED_SUFFIX="x")
        with pytest.raises(AssertionError, match="broke every re-import"):
            AbsenceGate([IMPORTED_SUFFIX]).check(namespace)

    def test_an_empty_gate_accepts_anything(self):
        """A gate with no recorded removals has nothing to enforce."""
        AbsenceGate([]).check(types.SimpleNamespace(IMPORTED_SUFFIX="x"))
