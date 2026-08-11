"""Tests for the Read-After-Write Wrapper pattern."""

import pytest

from design_patterns.gates.read_after_write import (
    InMemoryStore,
    WriteOutcome,
    WriteResult,
    apply_and_confirm,
)


class TestInMemoryStore:
    """Tests for the example store."""

    def test_a_plain_store_keeps_what_it_is_given(self):
        """The default store stores every field."""
        store = InMemoryStore({"assays/17": {"title": "old"}})
        store.apply("assays/17", {"title": "new"})
        assert store.read("assays/17") == {"title": "new"}

    def test_an_ignoring_store_drops_the_named_fields(self):
        """This is the behaviour the wrapper exists to detect."""
        store = InMemoryStore({"assays/17": {}}, ignored_fields={"data_files"})
        store.apply("assays/17", {"title": "new", "data_files": ["a"]})
        assert store.read("assays/17") == {"title": "new"}

    def test_a_refusing_store_raises(self):
        """A refusal is reported to the caller, unlike a discard."""
        store = InMemoryStore({"assays/17": {}}, refuses=True)
        with pytest.raises(RuntimeError):
            store.apply("assays/17", {"title": "new"})

    def test_reading_an_unknown_key_returns_nothing(self):
        """A missing record reads as empty rather than raising."""
        assert InMemoryStore({}).read("assays/99") == {}


class TestWriteResult:
    """Tests for the reported outcome."""

    def test_only_a_landed_write_is_ok(self):
        """ok is the single question most call sites ask."""
        landed = WriteResult(outcome=WriteOutcome.LANDED, message="")
        assert landed.ok is True

    def test_a_refusal_is_not_ok(self):
        """A visible failure is still a failure."""
        refused = WriteResult(outcome=WriteOutcome.REFUSED, message="")
        assert refused.ok is False

    def test_a_discard_is_not_ok(self):
        """An invisible failure must not read as success."""
        discarded = WriteResult(outcome=WriteOutcome.DISCARDED, message="")
        assert discarded.ok is False

    def test_refused_and_discarded_are_distinct_outcomes(self):
        """Collapsing them throws away the only information that says which."""
        assert WriteOutcome.REFUSED is not WriteOutcome.DISCARDED


class TestApplyAndConfirm:
    """Tests for the wrapper itself."""

    def test_a_stored_write_lands(self):
        """A write the store keeps is confirmed by the read-back."""
        store = InMemoryStore({"assays/17": {}})
        result = apply_and_confirm(store, "assays/17", {"data_files": ["a", "b"]})
        assert result.outcome is WriteOutcome.LANDED
        assert result.ok is True

    def test_a_rejected_write_is_refused(self):
        """An error from the store is a refusal, not a discard."""
        store = InMemoryStore({"assays/17": {}}, refuses=True)
        result = apply_and_confirm(store, "assays/17", {"data_files": ["a"]})
        assert result.outcome is WriteOutcome.REFUSED

    def test_a_silently_dropped_write_is_discarded(self):
        """The store answered success and stored nothing."""
        store = InMemoryStore({"assays/17": {}}, ignored_fields={"data_files"})
        result = apply_and_confirm(store, "assays/17", {"data_files": ["a", "b"]})
        assert result.outcome is WriteOutcome.DISCARDED

    def test_the_discarded_fields_are_reported(self):
        """Naming the fields is more useful than reporting that something failed."""
        store = InMemoryStore({"assays/17": {}}, ignored_fields={"data_files"})
        result = apply_and_confirm(
            store, "assays/17", {"title": "new", "data_files": ["a"]}
        )
        assert result.discarded == {"data_files": ["a"]}

    def test_a_partial_discard_does_not_report_the_fields_that_landed(self):
        """Only the fields that did not survive appear in the report."""
        store = InMemoryStore({"assays/17": {}}, ignored_fields={"data_files"})
        result = apply_and_confirm(
            store, "assays/17", {"title": "new", "data_files": ["a"]}
        )
        assert "title" not in result.discarded
        assert store.read("assays/17")["title"] == "new"

    def test_the_refusal_message_carries_the_error(self):
        """The visible failure keeps the store's own explanation."""
        store = InMemoryStore({"assays/17": {}}, refuses=True)
        result = apply_and_confirm(store, "assays/17", {"title": "new"})
        assert "refused" in result.message

    def test_the_discard_message_says_the_write_reported_success(self):
        """The message must distinguish this from an ordinary error."""
        store = InMemoryStore({"assays/17": {}}, ignored_fields={"data_files"})
        result = apply_and_confirm(store, "assays/17", {"data_files": ["a"]})
        assert "reported success" in result.message

    def test_an_empty_change_set_lands(self):
        """Writing nothing cannot be discarded."""
        store = InMemoryStore({"assays/17": {}}, ignored_fields={"data_files"})
        assert apply_and_confirm(store, "assays/17", {}).ok is True
