"""Tests for the Contract Gate pattern."""

import inspect

import pytest

from design_patterns.gates.contract import (
    ContractGate,
    DriftedDouble,
    FaithfulDouble,
    RealClient,
    signature_mismatches,
)

COVERED = ("get", "create")


class IncompleteDouble:
    """A stand-in that implements only part of the covered interface."""

    async def get(self, resource: str, identifier: int) -> dict[str, object]:
        """Return a stored record."""
        return {"resource": resource, "id": identifier}


class TestSignatureMismatches:
    """Tests for signature_mismatches."""

    def test_a_faithful_double_reports_nothing(self):
        """Matching parameter lists and asynchrony produce no messages."""
        assert signature_mismatches(RealClient, FaithfulDouble, COVERED) == []

    def test_a_renamed_parameter_is_reported(self):
        """Comparing names, not counts, catches renaming and reordering."""
        (message,) = signature_mismatches(RealClient, DriftedDouble, ["create"])
        assert "payload" in message
        assert "body" in message

    def test_a_double_that_stopped_being_async_is_reported(self):
        """A double that quietly becomes synchronous matches nothing real."""
        (message,) = signature_mismatches(RealClient, DriftedDouble, ["get"])
        assert "asynchronous" in message

    def test_a_missing_method_is_reported(self):
        """A covered method the substitute never implemented is drift too."""
        (message,) = signature_mismatches(RealClient, IncompleteDouble, ["create"])
        assert "does not implement it" in message

    def test_a_method_absent_from_the_real_class_is_reported(self):
        """A covered name that no longer exists means the list is stale."""
        (message,) = signature_mismatches(RealClient, FaithfulDouble, ["archive"])
        assert "absent from RealClient" in message

    def test_every_covered_method_is_checked(self):
        """Both drifted methods are reported in a single run."""
        assert len(signature_mismatches(RealClient, DriftedDouble, COVERED)) == 2

    def test_an_empty_covered_set_reports_nothing(self):
        """Checking no methods is vacuous rather than an error."""
        assert signature_mismatches(RealClient, DriftedDouble, []) == []


class TestContractGate:
    """Tests for ContractGate."""

    def test_a_faithful_double_passes(self):
        """The gate is quiet while the substitute still matches."""
        ContractGate(RealClient, FaithfulDouble, COVERED).check()

    def test_a_drifted_double_fails(self):
        """The gate fails once the substitute diverges."""
        gate = ContractGate(RealClient, DriftedDouble, COVERED)
        with pytest.raises(AssertionError):
            gate.check()

    def test_failure_names_the_drifted_methods(self):
        """The report identifies which methods diverged and how."""
        gate = ContractGate(RealClient, DriftedDouble, COVERED)
        with pytest.raises(AssertionError) as failure:
            gate.check()
        assert "get" in str(failure.value)
        assert "create" in str(failure.value)

    def test_violations_can_be_inspected_without_raising(self):
        """Parametrised tests need the messages, not an exception."""
        gate = ContractGate(RealClient, DriftedDouble, COVERED)
        assert len(gate.violations()) == 2

    @pytest.mark.parametrize("name", COVERED)
    def test_one_failure_per_method(self, name):
        """Parametrising reports each drifted method separately."""
        assert signature_mismatches(RealClient, FaithfulDouble, [name]) == []


class TestDemonstrationClasses:
    """Tests for the example client and its doubles."""

    def test_the_real_client_is_asynchronous(self):
        """The example exists to show asynchrony being part of the contract."""
        assert inspect.iscoroutinefunction(RealClient.get)
        assert inspect.iscoroutinefunction(RealClient.create)

    def test_the_drifted_double_is_the_documented_failure(self):
        """The example double drifts in exactly the two documented ways."""
        assert not inspect.iscoroutinefunction(DriftedDouble.get)
        assert "body" in inspect.signature(DriftedDouble.create).parameters
