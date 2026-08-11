"""Absence Gate: assert that a withdrawn name stays withdrawn.

The assertion in an absence gate carries almost no information on its own.
``assert not hasattr(module, "NAME")`` tells a future reader what is checked but
not why, and a check whose purpose is unclear is deleted as an obstacle. This
module therefore pairs each check with the date of the removal and the failure
that motivated it, and puts both into the failure message.
"""

from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class WithdrawnName:
    """A name removed on purpose, with the failure that caused the removal.

    Attributes:
        name: The attribute name that must not reappear.
        withdrawn_on: Date of the removal in YYMMDD format.
        reason: The failure the removal prevents, stated in the past tense.

    Example:
        ```python
        record = WithdrawnName(
            name="IMPORTED_SUFFIX",
            withdrawn_on="260806",
            reason="Deriving it from a mutable field broke every re-import.",
        )
        ```
    """

    name: str
    withdrawn_on: str
    reason: str

    def message(self) -> str:
        """Build the failure text for a reintroduction.

        Returns:
            str: Text naming the withdrawn name, the date, the original
                failure, and the action the reader should take.
        """
        return (
            f"{self.name} was withdrawn on {self.withdrawn_on} and has been "
            f"reintroduced. {self.reason} Remove it again, or record why the "
            f"original failure no longer applies."
        )


class AbsenceGate:
    """Fails when any withdrawn name is present in a namespace.

    Example:
        ```python
        legacy = WithdrawnName("LEGACY_MODE", "260701", "It had no callers.")
        AbsenceGate([legacy]).check(importer_module)
        ```
    """

    def __init__(self, withdrawn: Sequence[WithdrawnName]) -> None:
        """Record the names that must stay absent.

        Args:
            withdrawn: The removal decisions this gate enforces.
        """
        self._withdrawn = list(withdrawn)

    def violations(self, namespace: object) -> list[str]:
        """Find every withdrawn name present on a namespace.

        Args:
            namespace: A module, class, or object to inspect.

        Returns:
            list[str]: One message per reintroduced name, in the order the
                names were recorded.
        """
        return [
            entry.message()
            for entry in self._withdrawn
            if hasattr(namespace, entry.name)
        ]

    def check(self, namespace: object) -> None:
        """Assert that no withdrawn name is present.

        Args:
            namespace: A module, class, or object to inspect.

        Raises:
            AssertionError: If any withdrawn name has been reintroduced. The
                message lists every reintroduction with its recorded reason.
        """
        violations = self.violations(namespace)
        if violations:
            report = "\n".join(violations)
            raise AssertionError(report)
