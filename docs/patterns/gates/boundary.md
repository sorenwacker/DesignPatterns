# Boundary Gate

**Category:** Gate Pattern

## Overview

A boundary gate asserts that one layer does not know about another. A generic library must not import a specific profile; a domain layer must not import the web framework; an application must not reach into a library's internals outside one designated module. The rule is usually stated in a docstring and held only by discipline, which is why it erodes: each individual import looks reasonable in isolation.

Two refinements matter more than the import check itself: exempting the composition point explicitly, and checking the vocabulary as well as the imports.

## Concepts

### Composition Point

The one place whose job is to name the concrete implementation. Something has to. An exemption for the composition point is not debt, and keeping it in a different list from the debt exemptions is the point: one shrinks over time, the other does not. Merged, the list becomes noise and stops being maintained.

### Vocabulary Leakage

A layer can stay free of forbidden imports while its constants, defaults, and docstrings still name the thing it must not know about. The import check passes and the coupling is real, so the gate scans identifiers and string content as well as import statements.

### Hidden Dependency

The failure the rule prevents. A component that reaches out to find its collaborator — importing another layer to ask whether a context exists, resolving a global, probing for a running server — has a dependency no boundary test can express and no caller can substitute. A helper such as `default_profile()` that imports the profile package from inside the library is the canonical form.

## Usage Guidelines

**Use when:**

- A layering rule exists that only review discipline currently holds
- A library must remain free of any specific consumer's concerns
- An application is permitted to use a library's internals from one module only

**Avoid when:**

- The dependency direction is already enforced by packaging, so the import cannot resolve
- The layers are not yet distinct enough for the rule to be stated precisely
- Every module would need an exemption, which means the boundary is drawn in the wrong place

## Implementation

```python
import ast
from collections.abc import Mapping


class BoundaryGate:
    """Fails when a layer imports or names something it must not know about."""

    def __init__(
        self,
        forbidden_prefix: str,
        forbidden_vocabulary: frozenset[str],
        composition: frozenset[str],
        grandfathered: frozenset[str] = frozenset(),
    ) -> None:
        self._forbidden_prefix = forbidden_prefix
        self._forbidden_vocabulary = frozenset(
            word.lower() for word in forbidden_vocabulary
        )
        self._composition = frozenset(composition)
        self._grandfathered = frozenset(grandfathered)

    @property
    def composition(self) -> frozenset[str]:
        """Paths exempt on principle. This list does not shrink."""
        return self._composition

    @property
    def grandfathered(self) -> frozenset[str]:
        """Paths exempt as tolerated debt. This list should shrink."""
        return self._grandfathered

    def _exempt(self, path: str) -> bool:
        return path in self._composition or path in self._grandfathered

    def import_violations(self, sources: Mapping[str, str]) -> list[str]:
        """Messages for every forbidden import outside an exempt module."""
        violations = []
        for path, source in sorted(sources.items()):
            if self._exempt(path):
                continue
            for module in _imported_modules(source):
                if module == self._forbidden_prefix or module.startswith(
                    f"{self._forbidden_prefix}."
                ):
                    violations.append(
                        f"{path} imports {module}. The implementation is "
                        f"supplied by whoever composes the run, never reached for."
                    )
        return violations

    def vocabulary_violations(self, sources: Mapping[str, str]) -> list[str]:
        """Messages for forbidden words in identifiers, strings, or docstrings."""
        violations = []
        for path, source in sorted(sources.items()):
            if self._exempt(path):
                continue
            lowered = source.lower()
            violations.extend(
                f"{path} names {word!r} outside the composition point. "
                f"A layer free of the import can still be coupled by its vocabulary."
                for word in sorted(self._forbidden_vocabulary)
                if word in lowered
            )
        return violations

    def violations(self, sources: Mapping[str, str]) -> list[str]:
        """Every import and vocabulary violation."""
        return self.import_violations(sources) + self.vocabulary_violations(sources)


def _imported_modules(source: str) -> list[str]:
    """Every module named by an import statement in the source."""
    modules = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.append(node.module)
    return modules
```

### Usage

```python
GATE = BoundaryGate(
    forbidden_prefix="profiles",
    forbidden_vocabulary=frozenset({"miappe"}),
    composition=frozenset({"cli/__init__.py"}),
)

assert not GATE.violations(read_package_sources("library"))
```

## Trade-offs

**Benefits:**

1. Makes a layering rule enforceable rather than aspirational
2. Catches coupling through vocabulary that an import check alone misses
3. Distinguishes a principled exemption from unfinished work

**Drawbacks:**

1. Vocabulary matching produces false positives on words with ordinary meanings
2. Static import analysis does not see dynamic imports or plugin loading
3. Exemption lists invite growth when the boundary is inconvenient

## Real-World Examples

- Hexagonal or clean architecture checks asserting the domain imports no adapter
- Library tests failing when generic code imports a consumer-specific package
- Monorepo import linters restricting cross-package dependencies

## Related Patterns

- [Grandfathered-Debt Gate](grandfathered_debt.md) handles the debt list this gate keeps separate
- [Absence Gate](absence.md) prohibits a specific name rather than a whole layer
- [Population Gate](population.md) analyses source structure with the same technique

## API Reference

::: design_patterns.gates.boundary
    options:
      show_root_heading: true
      show_source: true
