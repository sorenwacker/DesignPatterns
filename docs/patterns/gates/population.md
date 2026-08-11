# Population Gate

**Category:** Gate Pattern

## Overview

A population gate asserts that only one of a kind exists. It applies where duplication itself is the defect rather than any individual instance being wrong: several hand-written test doubles for the same collaborator, several implementations of the same conversion, several places that parse the same format. The distinguishing feature of the pattern is that detection works on structure rather than on names, because names are chosen by people and people choose differently.

## Concepts

### Shape Detection

Identification by structure: the set of methods a class defines, the signature it exposes, the calls it makes. A search for `class _Fake` finds the doubles that happen to be named that way and misses the one called `MockClient`. A check on the method set finds both.

### Sanctioned Instance

The one member of the population that is allowed to exist. Naming it explicitly makes the gate a redirection rather than a prohibition: the failure message can say which implementation to use instead.

## Usage Guidelines

**Use when:**

- Duplication is the failure mode and the copies drift independently
- A shared implementation exists and new copies keep appearing beside it
- The duplicates are recognisable by structure even when named inconsistently

**Avoid when:**

- Multiple implementations are legitimate, such as several strategies behind one interface
- The shape is too common to discriminate, producing matches on unrelated code
- The population is small and stable enough that review catches additions

## Implementation

```python
import ast


class ClassShapeDetector:
    """Finds classes whose method set overlaps a reference set."""

    def __init__(self, methods: set[str], minimum_overlap: int = 2) -> None:
        self._methods = set(methods)
        self._minimum_overlap = minimum_overlap

    def matching_classes(self, source: str) -> list[str]:
        """Names of classes in the source whose methods overlap enough."""
        tree = ast.parse(source)
        matches = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            defined = {
                item.name
                for item in node.body
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
            }
            if len(defined & self._methods) >= self._minimum_overlap:
                matches.append(node.name)
        return matches


class PopulationGate:
    """Fails when more than the sanctioned implementation has a given shape."""

    def __init__(
        self,
        detector: ClassShapeDetector,
        sanctioned: set[str],
        replacement: str,
    ) -> None:
        self._detector = detector
        self._sanctioned = set(sanctioned)
        self._replacement = replacement

    def violations(self, sources: dict[str, str]) -> list[str]:
        """Messages for every unsanctioned class, naming its file."""
        return [
            f"{path}:{name} has the shape of the real collaborator; "
            f"use {self._replacement} instead."
            for path, source in sorted(sources.items())
            for name in self._detector.matching_classes(source)
            if name not in self._sanctioned
        ]
```

### Usage

```python
detector = ClassShapeDetector(
    methods={"get", "create", "update", "delete", "list_resources"},
    minimum_overlap=2,
)
gate = PopulationGate(
    detector,
    sanctioned={"FakeClient"},
    replacement="FakeClient from tests/doubles.py",
)

violations = gate.violations({"tests/test_import.py": source_text})
assert not violations, "\n".join(violations)
```

## Trade-offs

**Benefits:**

1. Finds instances that a name-based search misses
2. Names the sanctioned replacement, so the failure is a fix instruction
3. Resists evasion, because structure is harder to vary than naming

**Drawbacks:**

1. Requires tuning: too low an overlap threshold produces false matches, too high misses partial copies
2. Static analysis sees only what is written literally, missing classes built dynamically
3. The sanctioned set needs maintenance as the legitimate population changes

## Real-World Examples

- Test suites converging on one shared client double after accumulating hand-written ones
- Architecture checks asserting a single implementation of a serialisation format
- Codebase audits finding duplicated retry or backoff logic by call shape

## Related Patterns

- [Contract Gate](contract.md) checks the sanctioned instance against the real one
- [Absence Gate](absence.md) prohibits rather than consolidates
- [Boundary Gate](boundary.md) also analyses source structure rather than names

## API Reference

::: design_patterns.gates.population
    options:
      show_root_heading: true
      show_source: true
