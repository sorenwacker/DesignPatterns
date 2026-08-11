# Read-After-Write Wrapper

**Category:** Gate Pattern

## Overview

The read-after-write wrapper is the runtime form of a gate: it writes, reads back, compares, and reports the difference. Where the other gates run in a test suite, this one runs in production, catching what tests cannot be present for. It converts an entire class of silent data loss into a message, once, at the wrapper, rather than being remembered at each call site.

The distinguishing detail is that a refused write and a discarded write are separate outcomes. One is visible and one is not, and collapsing them into "it did not work" throws away the only information that says which.

## Concepts

### Refused

The write was rejected and the caller was told. The system reported an error, nothing changed, and the failure is already visible. The response is to handle the error.

### Discarded

The write was accepted, reported success, and stored nothing. The read-back does not match what was sent. This is the failure the wrapper exists to find, because nothing else reports it.

### Landed

The write was accepted and the read-back matches. The wrapper adds one read per write to establish this, which is the cost of the pattern.

## Usage Guidelines

**Use when:**

- A remote system is known to accept writes it does not store
- A silently lost write causes damage that is discovered much later
- The same write is issued from several call sites, each of which would otherwise need its own confirmation

**Avoid when:**

- The store is transactional and reports failures accurately
- The extra read is prohibitively expensive relative to the write
- The store is eventually consistent, so an immediate read-back is not evidence of anything

## Implementation

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol


class WriteOutcome(Enum):
    """Distinguishes a visible refusal from an invisible discard."""

    LANDED = "landed"
    REFUSED = "refused"
    DISCARDED = "discarded"


@dataclass(frozen=True)
class WriteResult:
    """The outcome of a write, with the fields that did not survive it."""

    outcome: WriteOutcome
    message: str
    discarded: dict[str, Any] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        """Whether the write landed."""
        return self.outcome is WriteOutcome.LANDED


class Store(Protocol):
    """The minimum a store must offer for the wrapper to confirm a write."""

    def apply(self, key: str, changes: dict[str, Any]) -> None: ...

    def read(self, key: str) -> dict[str, Any]: ...


def apply_and_confirm(store: Store, key: str, changes: dict[str, Any]) -> WriteResult:
    """Apply changes, read them back, and report what did not survive."""
    try:
        store.apply(key, changes)
    except Exception as error:  # the refusal is the information, not a surprise
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
    return WriteResult(outcome=WriteOutcome.LANDED, message=f"{key} accepted the write")
```

### Usage

```python
result = apply_and_confirm(store, "assays/17", {"data_files": ["a", "b"]})
if result.ok:
    return "assays/17"
report_warning(result.message)
return None
```

Keeping the outcomes distinct lets callers respond differently: a refusal is retried or surfaced as an error, while a discard is a defect in the remote system that needs reporting and a workaround.

## Trade-offs

**Benefits:**

1. Detects silently discarded writes, which no return code reports
2. Handles the confirmation once rather than at every call site
3. Names the specific fields that did not survive, not just that something failed

**Drawbacks:**

1. Doubles the request count for every write
2. Unreliable against eventually consistent stores, where an immediate read proves nothing
3. Comparison needs care where the store normalises values, causing false discards

## Real-World Examples

- Confirming relationship writes against APIs that accept and ignore them
- Verifying object storage uploads by reading back size and checksum
- Post-write validation in migration tools that must not lose records

## Related Patterns

- [Live Contract Gate](live_contract.md) is the test-suite form of the same check
- [Proxy](../structural/proxy.md) wraps access to an object in the same structural way
- [Decorator](../structural/decorator.md) adds the confirmation behaviour around an existing write

## API Reference

::: design_patterns.gates.read_after_write
    options:
      show_root_heading: true
      show_source: true
