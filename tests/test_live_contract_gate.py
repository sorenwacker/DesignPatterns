"""Tests for the Live Contract Gate pattern."""

import pytest

from design_patterns.gates.live_contract import LiveContractGate, ObservedBehaviour

SAMPLE_TYPES_DISCARDED = ObservedBehaviour(
    name="assay sample types after an API-created assay",
    observed=[],
    observed_on="260806",
    instruction=(
        "The server now returns sample types for an API-created assay. If it "
        "also accepts the relationship, the importer no longer needs sample "
        "types attached by hand; revisit ISAAssayService."
    ),
)


class TestObservedBehaviour:
    """Tests for the recorded observation."""

    def test_message_reports_both_values(self):
        """The report contrasts what was recorded with what is returned now."""
        message = SAMPLE_TYPES_DISCARDED.message(["dna"])
        assert "[]" in message
        assert "['dna']" in message

    def test_message_carries_the_date_of_the_observation(self):
        """A dated measurement stays checkable as the dependency changes."""
        assert "260806" in SAMPLE_TYPES_DISCARDED.message(["dna"])

    def test_message_says_what_to_do(self):
        """Asserting the defect turns the gate into a notification."""
        assert "revisit ISAAssayService" in SAMPLE_TYPES_DISCARDED.message(["dna"])

    def test_the_record_is_immutable(self):
        """An observation is a fact, not a mutable setting."""
        with pytest.raises(AttributeError):
            SAMPLE_TYPES_DISCARDED.observed_on = "260101"  # type: ignore[misc]


class TestConfiguration:
    """Tests for the configured skip."""

    def test_the_gate_is_inactive_without_credentials(self):
        """The ordinary suite must be unaffected by this gate."""
        assert LiveContractGate(None, None).configured is False

    def test_a_url_without_a_token_is_not_configured(self):
        """Both halves are needed before the gate can run."""
        assert LiveContractGate("https://example.test", None).configured is False

    def test_an_empty_value_does_not_configure_the_gate(self):
        """An unset environment variable often arrives as an empty string."""
        assert LiveContractGate("", "").configured is False

    def test_the_gate_is_active_with_both_values(self):
        """Supplying an instance activates the gate."""
        assert LiveContractGate("https://example.test", "token").configured is True

    def test_the_skip_reason_names_the_variables(self):
        """A skipped test must say how to run it."""
        reason = LiveContractGate(None, None).skip_reason()
        assert "CONTRACT_URL" in reason
        assert "CONTRACT_TOKEN" in reason


class TestCheck:
    """Tests for comparison against a live instance."""

    def test_unchanged_behaviour_passes(self):
        """While the dependency still behaves as recorded, the gate is quiet."""
        gate = LiveContractGate("https://example.test", "token")
        gate.check(SAMPLE_TYPES_DISCARDED, [])

    def test_changed_behaviour_fails(self):
        """The gate fires on the day the external behaviour changes."""
        gate = LiveContractGate("https://example.test", "token")
        with pytest.raises(AssertionError, match="revisit ISAAssayService"):
            gate.check(SAMPLE_TYPES_DISCARDED, ["dna"])

    def test_the_failure_reports_the_current_value(self):
        """The report shows what the system returns now."""
        gate = LiveContractGate("https://example.test", "token")
        with pytest.raises(AssertionError) as failure:
            gate.check(SAMPLE_TYPES_DISCARDED, ["dna"])
        assert "['dna']" in str(failure.value)

    def test_a_recorded_defect_is_asserted_as_found(self):
        """Recording an empty list asserts the discard, not the desired result."""
        assert SAMPLE_TYPES_DISCARDED.observed == []
