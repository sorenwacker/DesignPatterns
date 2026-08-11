"""Tests for the Population Gate pattern."""

import pytest

from design_patterns.gates.population import ClassShapeDetector, PopulationGate

CLIENT_METHODS = {"get", "create", "update", "delete", "list_resources"}

SANCTIONED_DOUBLE = """
class FakeClient:
    def get(self, resource, identifier): ...
    def create(self, resource, payload): ...
    def delete(self, resource, identifier): ...
"""

DIFFERENTLY_NAMED_DOUBLE = """
class MockClient:
    def get(self, resource, identifier): ...
    def update(self, resource, payload): ...
"""

UNRELATED_CLASS = """
class Report:
    def render(self): ...
    def get(self): ...
"""

ASYNC_DOUBLE = """
class AsyncStandIn:
    async def get(self, resource, identifier): ...
    async def create(self, resource, payload): ...
"""


@pytest.fixture
def detector():
    """A detector for classes shaped like the real client."""
    return ClassShapeDetector(methods=CLIENT_METHODS, minimum_overlap=2)


class TestClassShapeDetector:
    """Tests for shape-based detection."""

    def test_finds_a_class_by_its_method_set(self, detector):
        """Overlap with the reference methods is what identifies the class."""
        assert detector.matching_classes(SANCTIONED_DOUBLE) == ["FakeClient"]

    def test_finds_a_double_a_name_search_would_miss(self, detector):
        """A grep for _Fake misses MockClient; the shape check does not."""
        assert detector.matching_classes(DIFFERENTLY_NAMED_DOUBLE) == ["MockClient"]

    def test_ignores_a_class_below_the_overlap_threshold(self, detector):
        """One shared method name is coincidence, not a stand-in."""
        assert detector.matching_classes(UNRELATED_CLASS) == []

    def test_counts_asynchronous_methods(self, detector):
        """A double built from coroutines has the same shape as one that is not."""
        assert detector.matching_classes(ASYNC_DOUBLE) == ["AsyncStandIn"]

    def test_threshold_is_configurable(self):
        """Raising the threshold narrows what counts as the same shape."""
        strict = ClassShapeDetector(methods=CLIENT_METHODS, minimum_overlap=3)
        assert strict.matching_classes(DIFFERENTLY_NAMED_DOUBLE) == []
        assert strict.matching_classes(SANCTIONED_DOUBLE) == ["FakeClient"]

    def test_finds_every_matching_class_in_one_source(self, detector):
        """A file holding two doubles reports both."""
        source = SANCTIONED_DOUBLE + DIFFERENTLY_NAMED_DOUBLE
        assert detector.matching_classes(source) == ["FakeClient", "MockClient"]

    def test_a_source_with_no_classes_matches_nothing(self, detector):
        """Parsing plain module code yields no candidates."""
        assert detector.matching_classes("value = get()\n") == []


class TestPopulationGate:
    """Tests for PopulationGate."""

    @pytest.fixture
    def gate(self, detector):
        """A gate permitting only FakeClient."""
        return PopulationGate(
            detector,
            sanctioned={"FakeClient"},
            replacement="FakeClient from tests/doubles.py",
        )

    def test_the_sanctioned_double_is_permitted(self, gate):
        """Exactly one implementation is allowed to have the shape."""
        assert gate.violations({"tests/doubles.py": SANCTIONED_DOUBLE}) == []

    def test_an_unsanctioned_double_is_a_violation(self, gate):
        """A second implementation of the same shape is the failure mode."""
        violations = gate.violations({"tests/test_import.py": DIFFERENTLY_NAMED_DOUBLE})
        assert len(violations) == 1

    def test_violation_names_the_file_and_the_class(self, gate):
        """The message must locate the offender."""
        (message,) = gate.violations({"tests/test_import.py": DIFFERENTLY_NAMED_DOUBLE})
        assert "tests/test_import.py" in message
        assert "MockClient" in message

    def test_violation_names_the_replacement(self, gate):
        """The message is a redirection, not only a prohibition."""
        (message,) = gate.violations({"tests/test_import.py": DIFFERENTLY_NAMED_DOUBLE})
        assert "FakeClient from tests/doubles.py" in message

    def test_violations_are_reported_in_file_order(self, gate):
        """Stable ordering keeps the failure output readable across runs."""
        violations = gate.violations(
            {
                "tests/b_test.py": ASYNC_DOUBLE,
                "tests/a_test.py": DIFFERENTLY_NAMED_DOUBLE,
            }
        )
        assert "tests/a_test.py" in violations[0]
        assert "tests/b_test.py" in violations[1]

    def test_check_raises_listing_every_offender(self, gate):
        """One failure reports the whole population, not the first member."""
        with pytest.raises(AssertionError) as failure:
            gate.check(
                {"tests/a.py": DIFFERENTLY_NAMED_DOUBLE, "tests/b.py": ASYNC_DOUBLE}
            )
        assert "MockClient" in str(failure.value)
        assert "AsyncStandIn" in str(failure.value)

    def test_check_passes_on_a_clean_suite(self, gate):
        """A suite with only the sanctioned double passes quietly."""
        gate.check({"tests/doubles.py": SANCTIONED_DOUBLE})
