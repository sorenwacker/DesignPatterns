# Absence Gate

**Category:** Gate Pattern

## Overview

An absence gate asserts that something removed from a codebase stays removed. It is the simplest gate to write and the one whose assertion carries the least information: `assert not hasattr(module, "NAME")` tells a future reader what is checked but nothing about why. The value of the pattern lies in the recorded reason, which is what stops a withdrawn name from being reintroduced by someone who never learned why it went.

## Concepts

### Withdrawn Name

A record of something deliberately removed: the name, the date it was withdrawn, and the failure that motivated the removal. The date and the failure are the payload; the name alone is recoverable from the assertion.

### Reintroduction

The failure mode the gate detects. A withdrawn name reappears because the absence looked like an oversight rather than a decision. Without a recorded reason, reintroduction is indistinguishable from a missing feature being supplied.

## Usage Guidelines

**Use when:**

- Something was deleted for a reason that is not obvious from its absence
- A feature was withdrawn after causing a failure that would recur if it returned
- A name encoded an assumption that turned out to be wrong

**Avoid when:**

- The absence is self-evident, such as a name the type checker or a compiler would reject
- The removal was cosmetic, such as a rename with no behavioural consequence
- The construct cannot be reintroduced by accident because nothing in the design has a place for it

## Implementation

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class WithdrawnName:
    """A name removed on purpose, with the failure that caused the removal."""

    name: str
    withdrawn_on: str
    reason: str

    def message(self) -> str:
        """Failure text naming the date and the original failure."""
        return (
            f"{self.name} was withdrawn on {self.withdrawn_on} and has been "
            f"reintroduced. {self.reason} Remove it again, or record why the "
            f"original failure no longer applies."
        )


class AbsenceGate:
    """Fails when any withdrawn name is present in a namespace."""

    def __init__(self, withdrawn: list[WithdrawnName]) -> None:
        self._withdrawn = list(withdrawn)

    def violations(self, namespace: object) -> list[str]:
        """Messages for every withdrawn name found on the namespace."""
        return [
            entry.message()
            for entry in self._withdrawn
            if hasattr(namespace, entry.name)
        ]

    def check(self, namespace: object) -> None:
        """Raise AssertionError listing every reintroduced name."""
        violations = self.violations(namespace)
        if violations:
            raise AssertionError("\n".join(violations))
```

### Usage

```python
IMPORT_SUFFIX = WithdrawnName(
    name="IMPORTED_SUFFIX",
    withdrawn_on="260806",
    reason=(
        "The suffix described how a record reached the system rather than what "
        "it was, and deriving it from a mutable field broke every re-import "
        "after a rename."
    ),
)

gate = AbsenceGate([IMPORT_SUFFIX])
gate.check(importer_module)  # raises if IMPORTED_SUFFIX is back
```

## Trade-offs

**Benefits:**

1. Converts a deletion decision into a check the build enforces
2. Carries the original failure forward to whoever next considers the feature
3. Costs almost nothing to write and to run

**Drawbacks:**

1. Detects reintroduction under the original name only; the same idea under a new name passes
2. Accumulates entries that eventually describe a codebase nobody remembers
3. Reads as an obstacle when the reason is missing or vague, inviting deletion of the gate itself

## Real-World Examples

- Deprecation gates that fail when a removed configuration key reappears
- Lint rules banning an API that caused a production incident
- Database migration checks asserting that a dropped column is not recreated

## Related Patterns

- [Population Gate](population.md) detects unwanted duplication rather than unwanted return
- [Boundary Gate](boundary.md) applies the same recorded-reason discipline to layering
- [Grandfathered-Debt Gate](grandfathered_debt.md) records measurements where this records decisions

## API Reference

::: design_patterns.gates.absence
    options:
      show_root_heading: true
      show_source: true
