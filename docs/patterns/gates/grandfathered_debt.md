# Grandfathered-Debt Gate

**Category:** Gate Pattern

## Overview

A grandfathered-debt gate applies a limit from a chosen date forward while tolerating the violations that already existed. It is the pattern for a rule that is right but cannot be retrofitted in one proportionate change: a module length cap adopted against a codebase that already exceeds it, a type coverage threshold, a lint rule with a backlog. New violations fail; recorded ones may shrink but never grow.

## Concepts

### Recorded Measurement

The measured value of each existing violation on the date the gate was added, not a description of it. "It was 1191 lines on 260806" is a fact that stays checkable; "this file is too long" is an opinion that ages badly.

### Three Checks

The gate needs all three to remain honest:

1. **New violations fail.** Anything over the cap that is not recorded is a new violation.
2. **Recorded debt cannot grow.** A recorded entry that exceeds its recorded value fails.
3. **Stale entries fail.** A recorded entry that now passes the cap must be removed.

The third is the one most often left out and the one that keeps the list credible. After a module is split, a forgotten entry makes the debt look worse than it is, and a list known to be wrong stops being read.

## Usage Guidelines

**Use when:**

- The rule is correct but the codebase already violates it in many places
- Fixing every violation in one change would be disproportionate or risky
- Progress should be ratcheted: improvement is permitted, regression is not

**Avoid when:**

- The violations are few enough to fix in the change that adopts the rule
- The measurement is unstable, so entries would need constant revision
- The limit is arbitrary and the list would grow rather than shrink

## Implementation

```python
from collections.abc import Mapping


class GrandfatheredLimit:
    """A cap that new code must meet and recorded violations may not exceed."""

    def __init__(self, cap: int, recorded: Mapping[str, int], recorded_on: str) -> None:
        self._cap = cap
        self._recorded = dict(recorded)
        self._recorded_on = recorded_on

    def new_violations(self, measurements: Mapping[str, int]) -> list[str]:
        """Modules over the cap that were not recorded when it was adopted."""
        return [
            f"{name} measures {value}, over the cap of {self._cap}. "
            f"Bring it under the cap; the allow list is closed."
            for name, value in sorted(measurements.items())
            if value > self._cap and name not in self._recorded
        ]

    def worsened(self, measurements: Mapping[str, int]) -> list[str]:
        """Recorded modules that have grown since the cap was adopted."""
        return [
            f"{name} measured {self._recorded[name]} on {self._recorded_on} "
            f"and now measures {value}. Recorded debt may shrink, not grow."
            for name, value in sorted(measurements.items())
            if name in self._recorded and value > self._recorded[name]
        ]

    def stale_entries(self, measurements: Mapping[str, int]) -> list[str]:
        """Recorded modules that now pass the cap and should be removed."""
        return [
            f"{name} measures {measurements[name]} and now passes the cap of "
            f"{self._cap}. Delete its entry so the list stays accurate."
            for name in sorted(self._recorded)
            if name in measurements and measurements[name] <= self._cap
        ]

    def violations(self, measurements: Mapping[str, int]) -> list[str]:
        """Every violation across the three checks."""
        return (
            self.new_violations(measurements)
            + self.worsened(measurements)
            + self.stale_entries(measurements)
        )
```

### Usage

```python
LIMIT = GrandfatheredLimit(
    cap=666,
    # Module -> its length when this gate was added. Lower a number when the
    # module shrinks; delete the entry when it passes the cap.
    recorded={"pkg/metadata_definitions.py": 1191, "pkg/importer/isa.py": 842},
    recorded_on="260806",
)

assert not LIMIT.violations(measure_module_lengths())
```

Splitting the three checks into three tests reports the three failures separately, which matters because they call for different responses: shorten the module, revert the growth, or prune the list.

## Trade-offs

**Benefits:**

1. Allows adopting a correct rule without a large retrofit
2. Ratchets in one direction, so the debt is bounded and decreasing
3. Records measured facts with dates, which stay checkable as the code changes

**Drawbacks:**

1. The allow list is a second thing to maintain and can be extended under pressure
2. Measurements are noisy for some metrics, causing failures unrelated to the rule
3. Tolerated violations can persist indefinitely if nothing schedules the work

## Real-World Examples

- Module or file length caps adopted against an existing codebase
- Type checker strictness raised per module with a shrinking exclusion list
- Lint rules enabled with a baseline file of pre-existing findings

## Related Patterns

- [Boundary Gate](boundary.md) uses a similar list, but separates principle from debt
- [Absence Gate](absence.md) records a decision where this records a measurement
- [Population Gate](population.md) bounds a count rather than a per-item measurement

## API Reference

::: design_patterns.gates.grandfathered_debt
    options:
      show_root_heading: true
      show_source: true
