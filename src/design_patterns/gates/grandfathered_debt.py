"""Grandfathered-Debt Gate: apply a limit forward over existing violations.

This is the pattern for a rule that is right but cannot be retrofitted in one
proportionate change. New violations fail; recorded ones may shrink but never
grow; and entries that now pass the cap must be deleted, which is the check most
often left out and the one that keeps the list credible. After a module is split,
a forgotten entry makes the debt look worse than it is, and a list known to be
wrong stops being read.

Entries record a measured value and a date. "It was 1191 on 260806" is a fact
that stays checkable; "this file is too long" is an opinion that ages badly.
"""

from collections.abc import Mapping


class GrandfatheredLimit:
    """A cap that new code must meet and recorded violations may not exceed.

    Example:
        ```python
        limit = GrandfatheredLimit(
            cap=666,
            recorded={"pkg/metadata_definitions.py": 1191},
            recorded_on="260806",
        )
        limit.check(measure_module_lengths())
        ```
    """

    def __init__(
        self,
        cap: int,
        recorded: Mapping[str, int],
        recorded_on: str,
    ) -> None:
        """Adopt a limit over a codebase that already violates it.

        Args:
            cap: The largest permitted measurement.
            recorded: Existing violations mapped to their measured value on
                the day the limit was adopted.
            recorded_on: That date, in YYMMDD format.
        """
        self._cap = cap
        self._recorded = dict(recorded)
        self._recorded_on = recorded_on

    def new_violations(self, measurements: Mapping[str, int]) -> list[str]:
        """Find modules over the cap that were not recorded at adoption.

        Args:
            measurements: Current measurement per module.

        Returns:
            list[str]: One message per new violation, ordered by module name.
        """
        return [
            f"{name} measures {value}, over the cap of {self._cap}. Bring it "
            f"under the cap; the allow list is closed."
            for name, value in sorted(measurements.items())
            if value > self._cap and name not in self._recorded
        ]

    def worsened(self, measurements: Mapping[str, int]) -> list[str]:
        """Find recorded modules that have grown since adoption.

        Args:
            measurements: Current measurement per module.

        Returns:
            list[str]: One message per regression, quoting the recorded value
                and the date it was measured.
        """
        return [
            f"{name} measured {self._recorded[name]} on {self._recorded_on} and "
            f"now measures {value}. Recorded debt may shrink, not grow."
            for name, value in sorted(measurements.items())
            if name in self._recorded and value > self._recorded[name]
        ]

    def stale_entries(self, measurements: Mapping[str, int]) -> list[str]:
        """Find recorded modules that now pass the cap.

        Args:
            measurements: Current measurement per module. Modules absent from
                this mapping say nothing about their entry and are skipped.

        Returns:
            list[str]: One message per entry that should be deleted.
        """
        return [
            f"{name} measures {measurements[name]} and now passes the cap of "
            f"{self._cap}. Delete its entry so the list stays accurate."
            for name in sorted(self._recorded)
            if name in measurements and measurements[name] <= self._cap
        ]

    def violations(self, measurements: Mapping[str, int]) -> list[str]:
        """Run all three checks.

        Args:
            measurements: Current measurement per module.

        Returns:
            list[str]: New violations, then regressions, then stale entries.
        """
        return (
            self.new_violations(measurements)
            + self.worsened(measurements)
            + self.stale_entries(measurements)
        )

    def check(self, measurements: Mapping[str, int]) -> None:
        """Assert that the codebase is within the ratchet.

        Splitting the three checks into three separate tests is usually better,
        because the three failures call for different responses: shorten the
        module, revert the growth, or prune the list.

        Args:
            measurements: Current measurement per module.

        Raises:
            AssertionError: If any of the three checks finds a violation.
        """
        violations = self.violations(measurements)
        if violations:
            report = "\n".join(violations)
            raise AssertionError(report)
