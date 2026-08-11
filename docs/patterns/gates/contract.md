# Contract Gate

**Category:** Gate Pattern

## Overview

A contract gate asserts that a stand-in matches the thing it stands in for. Test doubles drift from the real collaborator silently: a parameter is added to the real client and not to the double, or an asynchronous method becomes synchronous in the substitute. Both cases leave the suite green while every test runs against an interface the production code no longer has.

## Concepts

### Signature Correspondence

The parameter names and order of a substitute method compared against the real one. Comparing names rather than counts catches reordering and renaming, which are the changes that pass a count check and break callers.

### Asynchrony as Part of the Contract

Whether a method is a coroutine function is part of its signature. A double that quietly becomes synchronous satisfies every assertion about return values and matches nothing the runtime does.

### Eliminating the Substitute

The stronger form of the pattern. Where hand-written doubles set derived attributes directly, tests assert against a value shape the real system never produces. Returning genuine value objects makes that class of drift impossible rather than merely detectable, which is better than any gate.

## Usage Guidelines

**Use when:**

- A test double, stub, or fake stands in for a real collaborator
- Two implementations must remain interface-compatible across versions
- A protocol or interface has implementations maintained separately from it

**Avoid when:**

- The substitute can be removed entirely in favour of the real value type
- The double intentionally implements a narrower interface, documented as such
- The real object is itself unstable and the double encodes a deliberate target shape

## Implementation

```python
import inspect
from collections.abc import Sequence


def signature_mismatches(
    real: type,
    substitute: type,
    covered: Sequence[str],
) -> list[str]:
    """Differences between a substitute's methods and the real ones."""
    problems = []
    for name in covered:
        real_method = getattr(real, name, None)
        fake_method = getattr(substitute, name, None)
        if real_method is None:
            problems.append(
                f"{name}: absent from {real.__name__}. Remove it from the "
                f"covered set or restore it."
            )
            continue
        if fake_method is None:
            problems.append(
                f"{name}: {substitute.__name__} does not implement it; "
                f"add it or narrow the covered set."
            )
            continue

        real_params = list(inspect.signature(real_method).parameters)
        fake_params = list(inspect.signature(fake_method).parameters)
        if real_params != fake_params:
            problems.append(
                f"{name}: {substitute.__name__} takes {fake_params}, "
                f"{real.__name__} takes {real_params}."
            )

        real_async = inspect.iscoroutinefunction(real_method)
        fake_async = inspect.iscoroutinefunction(fake_method)
        if real_async != fake_async:
            expected = "asynchronous" if real_async else "synchronous"
            problems.append(
                f"{name}: {real.__name__} is {expected} and "
                f"{substitute.__name__} is not."
            )
    return problems


class ContractGate:
    """Fails when a substitute has drifted from the real collaborator."""

    def __init__(self, real: type, substitute: type, covered: Sequence[str]) -> None:
        self._real = real
        self._substitute = substitute
        self._covered = list(covered)

    def violations(self) -> list[str]:
        """Messages for every method that does not correspond."""
        return signature_mismatches(self._real, self._substitute, self._covered)

    def check(self) -> None:
        """Raise AssertionError describing every drifted method."""
        violations = self.violations()
        if violations:
            raise AssertionError("\n".join(violations))
```

### Usage

```python
COVERED = ("get", "create")

gate = ContractGate(RealClient, FakeClient, COVERED)
gate.check()  # raises when a parameter list or asynchrony diverges
```

Parametrising over the covered methods gives one failure per drifted method rather than one aggregate failure:

```python
@pytest.mark.parametrize("name", COVERED)
def test_the_signature_matches_the_real_client(name):
    """A double whose signature drifts passes every test and matches nothing."""
    assert not signature_mismatches(RealClient, FakeClient, [name])
```

## Trade-offs

**Benefits:**

1. Catches drift at the point of change rather than in production
2. Covers asynchrony, which return-value assertions cannot detect
3. Names the specific method and the specific difference

**Drawbacks:**

1. Verifies shape, not behaviour: a matching signature can still do the wrong thing
2. Needs an explicit covered set, which can fall behind the real interface
3. Encourages keeping a double that would be better deleted

## Real-World Examples

- Fake API clients checked against the real client class in a test suite
- Protocol conformance tests comparing implementations against a reference
- Mock frameworks offering signature-checked autospec doubles

## Related Patterns

- [Population Gate](population.md) reduces the doubles to the one this gate checks
- [Live Contract Gate](live_contract.md) checks the real collaborator against the outside world
- [Absence Gate](absence.md) records the removal when a substitute is deleted rather than checked

## API Reference

::: design_patterns.gates.contract
    options:
      show_root_heading: true
      show_source: true
