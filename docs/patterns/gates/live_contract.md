# Live Contract Gate

**Category:** Gate Pattern

## Overview

A live contract gate asserts that what the code believes about an external system is true of that system. It is the one gate a mocked suite cannot be: a suite built on doubles verifies the code against its own assumptions, and a wrong assumption is invisible from the inside. The gate runs against a real instance, is skipped unless one is configured, and asserts what was observed rather than what would be preferred.

## Concepts

### Configured Skip

The gate is disabled unless connection details are supplied through the environment, so the ordinary suite is unaffected and continuous integration minutes are not spent on it. Run it before a release, after upgrading the dependency, and when a write appears to succeed while nothing changes.

### Asserting the Observed Behaviour

The assertion records what the system actually does, including where that is defective, together with the instruction to follow when it changes. Asserting the defect turns the gate into a notification: it fails on the day the behaviour is fixed, and the message says what to do about it. Asserting the desired behaviour instead produces a test that fails continuously and is disabled.

### Exercising the Real Code Path

The gate calls the project's own client rather than issuing a hand-rolled request. A client reporting `403 Forbidden` on deletes that a plain request performs happily is a defect in the client, and a test that issues its own request stays green while the tool tells users records cannot be removed.

## Usage Guidelines

**Use when:**

- A dependency can fail silently, accepting a write and discarding it
- A dependency reports an error that is not real
- An assumption about an external system is load-bearing and unverified

**Avoid when:**

- The dependency has a specification and a conformance suite already covering it
- No instance can be reached from where tests run, and none can be provisioned
- The behaviour is already covered by an integration test in the ordinary suite

## Implementation

```python
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ObservedBehaviour:
    """What an external system was measured to do, and what to do when it changes."""

    name: str
    observed: Any
    observed_on: str
    instruction: str

    def message(self, current: Any) -> str:
        """Failure text reporting the change and the action it calls for."""
        return (
            f"{self.name} returned {self.observed!r} on {self.observed_on} and "
            f"now returns {current!r}. {self.instruction}"
        )


class LiveContractGate:
    """Compares recorded external behaviour against a live instance."""

    def __init__(
        self,
        url: str | None,
        token: str | None,
        url_variable: str = "CONTRACT_URL",
        token_variable: str = "CONTRACT_TOKEN",
    ) -> None:
        self._url = url
        self._token = token
        self._url_variable = url_variable
        self._token_variable = token_variable

    @property
    def configured(self) -> bool:
        """Whether an instance is available to run against."""
        return bool(self._url) and bool(self._token)

    def skip_reason(self) -> str:
        """Why the gate is inactive, naming the variables that activate it."""
        return (
            f"set {self._url_variable} and {self._token_variable} to run "
            f"against an instance"
        )

    def check(self, recorded: ObservedBehaviour, current: Any) -> None:
        """Raise AssertionError when the system no longer behaves as recorded."""
        if current != recorded.observed:
            raise AssertionError(recorded.message(current))
```

### Usage

```python
GATE = LiveContractGate(os.environ.get("CONTRACT_URL"), os.environ.get("CONTRACT_TOKEN"))

pytestmark = pytest.mark.skipif(not GATE.configured, reason=GATE.skip_reason())

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


def test_the_server_still_discards_sample_types():
    """The write is accepted, answered 200, and stored nowhere."""
    assay = client.create_assay(sample_types=["dna"])  # our client, not a raw request
    GATE.check(SAMPLE_TYPES_DISCARDED, client.get_assay(assay.id).sample_types)
```

## Trade-offs

**Benefits:**

1. Detects silent acceptance and discard, which no mocked test can observe
2. Notifies when an external defect is fixed, rather than failing until it is
3. Exercises the project's own client, so client defects surface too

**Drawbacks:**

1. Requires a reachable instance and credentials, so it does not run by default
2. Being skipped by default, it can go unrun for long periods
3. Writes against a real system need cleanup and can interfere with other users

## Real-World Examples

- Contract tests run against a staging API before a release
- Provider verification in consumer-driven contract testing
- Compatibility suites run after upgrading a database or client library

## Related Patterns

- [Read-After-Write Wrapper](read_after_write.md) is the runtime form of the same check
- [Contract Gate](contract.md) checks internal substitutes rather than the external system
- [Absence Gate](absence.md) records the removal when a workaround is finally dropped

## API Reference

::: design_patterns.gates.live_contract
    options:
      show_root_heading: true
      show_source: true
