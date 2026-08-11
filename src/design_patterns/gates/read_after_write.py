"""Read-After-Write Wrapper: confirm at runtime that a write landed.

Where the other gates run in a test suite, this one runs in production, catching
what tests cannot be present for. It writes, reads back, compares, and reports
the difference, converting an entire class of silent data loss into a message
once at the wrapper rather than being remembered at each call site.

A refused write and a discarded write are kept as separate outcomes. One is
visible and one is not, and collapsing them into "it did not work" throws away
the only information that says which.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol


class WriteOutcome(Enum):
    """Distinguishes a visible refusal from an invisible discard.

    Attributes:
        LANDED: The store accepted the write and the read-back matches.
        REFUSED: The store rejected the write and said so.
        DISCARDED: The store reported success and stored nothing.
    """

    LANDED = "landed"
    REFUSED = "refused"
    DISCARDED = "discarded"


@dataclass(frozen=True)
class WriteResult:
    """The outcome of a write, with the fields that did not survive it.

    Attributes:
        outcome: Which of the three outcomes occurred.
        message: Text describing the outcome, suitable for a warning.
        discarded: Fields that were sent but are absent from the read-back,
            mapped to the values that were sent.
    """

    outcome: WriteOutcome
    message: str
    discarded: dict[str, Any] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        """Whether the write landed."""
        return self.outcome is WriteOutcome.LANDED


class Store(Protocol):
    """The minimum a store must offer for a write to be confirmed."""

    def apply(self, key: str, changes: dict[str, Any]) -> None:
        """Write field values to a record.

        Args:
            key: Identifier of the record.
            changes: Field values to write.
        """
        ...

    def read(self, key: str) -> dict[str, Any]:
        """Read a record back.

        Args:
            key: Identifier of the record.

        Returns:
            dict[str, Any]: The stored field values.
        """
        ...


class InMemoryStore:
    """A store that can demonstrate each of the three outcomes.

    Example:
        ```python
        store = InMemoryStore({"assays/17": {}}, ignored_fields={"data_files"})
        apply_and_confirm(store, "assays/17", {"data_files": ["a"]})
        ```
    """

    def __init__(
        self,
        records: dict[str, dict[str, Any]],
        ignored_fields: set[str] | None = None,
        refuses: bool = False,
    ) -> None:
        """Configure how the store treats writes.

        Args:
            records: Initial contents, mapping key to stored field values.
            ignored_fields: Fields the store accepts and silently drops, which
                is the behaviour the wrapper exists to detect.
            refuses: Whether the store rejects every write with an error.
        """
        self._records = records
        self._ignored_fields = set(ignored_fields or set())
        self._refuses = refuses

    def apply(self, key: str, changes: dict[str, Any]) -> None:
        """Write field values, dropping the ignored ones without complaint.

        Args:
            key: Identifier of the record.
            changes: Field values to write.

        Raises:
            RuntimeError: If the store is configured to refuse writes.
        """
        if self._refuses:
            message = f"the store rejected the write to {key}"
            raise RuntimeError(message)
        stored = self._records.setdefault(key, {})
        stored.update(
            {
                name: value
                for name, value in changes.items()
                if name not in self._ignored_fields
            }
        )

    def read(self, key: str) -> dict[str, Any]:
        """Read a record back.

        Args:
            key: Identifier of the record.

        Returns:
            dict[str, Any]: The stored field values, empty for an unknown key.
        """
        return dict(self._records.get(key, {}))


def apply_and_confirm(store: Store, key: str, changes: dict[str, Any]) -> WriteResult:
    """Apply changes, read them back, and report what did not survive.

    Args:
        store: The store to write to and read from.
        key: Identifier of the record.
        changes: Field values to write.

    Returns:
        WriteResult: LANDED when the read-back matches, REFUSED when the store
            reported an error, and DISCARDED when the store reported success but
            the values are absent.
    """
    try:
        store.apply(key, changes)
    except Exception as error:
        return WriteResult(
            outcome=WriteOutcome.REFUSED,
            message=f"{key} refused the write: {error}",
        )

    stored = store.read(key)
    discarded = {
        name: value for name, value in changes.items() if stored.get(name) != value
    }
    if discarded:
        return WriteResult(
            outcome=WriteOutcome.DISCARDED,
            message=(
                f"{key} accepted the write and stored none of {sorted(discarded)}. "
                f"The write reported success; the record did not change."
            ),
            discarded=discarded,
        )
    return WriteResult(
        outcome=WriteOutcome.LANDED,
        message=f"{key} accepted the write",
    )
