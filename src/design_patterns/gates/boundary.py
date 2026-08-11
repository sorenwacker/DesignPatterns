"""Boundary Gate: assert that one layer does not know about another.

Two refinements matter more than the import check itself.

The composition point is exempt on principle. Something has to name the concrete
implementation, and that place is not debt. Keeping it in a different list from
the tolerated violations is the point: one list shrinks over time, the other does
not, and merged they become noise that stops being maintained.

The vocabulary is checked as well as the imports. A layer can stay free of
forbidden imports while its constants, defaults, and docstrings still name the
thing it must not know about.
"""

import ast
from collections.abc import Mapping


def _imported_modules(source: str) -> list[str]:
    """Collect every module named by an import statement.

    Args:
        source: Python source text to parse.

    Returns:
        list[str]: Module names from both ``import`` and ``from`` statements.
    """
    modules: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.append(node.module)
    return modules


class BoundaryGate:
    """Fails when a layer imports or names something it must not know about.

    Example:
        ```python
        gate = BoundaryGate(
            forbidden_prefix="profiles",
            forbidden_vocabulary=frozenset({"miappe"}),
            composition=frozenset({"cli/__init__.py"}),
        )
        gate.check(read_package_sources("library"))
        ```
    """

    def __init__(
        self,
        forbidden_prefix: str,
        forbidden_vocabulary: frozenset[str],
        composition: frozenset[str],
        grandfathered: frozenset[str] = frozenset(),
    ) -> None:
        """Draw the boundary and record both kinds of exemption.

        Args:
            forbidden_prefix: Package the checked layer may not import, matched
                on the module path so submodules are covered too.
            forbidden_vocabulary: Words the checked layer may not use anywhere
                in its source, matched case-insensitively.
            composition: Paths exempt on principle, where naming the concrete
                implementation is the module's job.
            grandfathered: Paths exempt as debt. These are not allowed, they are
                merely not fixed yet, and the list should shrink.
        """
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
        """Report whether a path is exempt for either reason.

        Args:
            path: The module path being checked.

        Returns:
            bool: True if the path is a composition point or grandfathered.
        """
        return path in self._composition or path in self._grandfathered

    def _crosses_boundary(self, module: str) -> bool:
        """Report whether an imported module lies beyond the boundary.

        Args:
            module: The imported module path.

        Returns:
            bool: True for the forbidden package itself and anything under it,
                and False for packages that merely share a name prefix.
        """
        return module == self._forbidden_prefix or module.startswith(
            f"{self._forbidden_prefix}."
        )

    def import_violations(self, sources: Mapping[str, str]) -> list[str]:
        """Find forbidden imports outside the exempt modules.

        Args:
            sources: Mapping of module path to Python source text.

        Returns:
            list[str]: One message per forbidden import, ordered by path.
        """
        violations: list[str] = []
        for path, source in sorted(sources.items()):
            if self._exempt(path):
                continue
            violations.extend(
                f"{path} imports {module}. The implementation is supplied by "
                f"whoever composes the run, never reached for."
                for module in _imported_modules(source)
                if self._crosses_boundary(module)
            )
        return violations

    def vocabulary_violations(self, sources: Mapping[str, str]) -> list[str]:
        """Find forbidden words in identifiers, strings, and docstrings.

        Args:
            sources: Mapping of module path to Python source text.

        Returns:
            list[str]: One message per forbidden word per file, ordered by path
                then by word.
        """
        violations: list[str] = []
        for path, source in sorted(sources.items()):
            if self._exempt(path):
                continue
            lowered = source.lower()
            violations.extend(
                f"{path} names {word!r} outside the composition point. A layer "
                f"free of the import can still be coupled by its vocabulary."
                for word in sorted(self._forbidden_vocabulary)
                if word in lowered
            )
        return violations

    def violations(self, sources: Mapping[str, str]) -> list[str]:
        """Run both halves of the gate.

        Args:
            sources: Mapping of module path to Python source text.

        Returns:
            list[str]: Import violations followed by vocabulary violations.
        """
        return self.import_violations(sources) + self.vocabulary_violations(sources)

    def check(self, sources: Mapping[str, str]) -> None:
        """Assert that the layer honours the boundary.

        Args:
            sources: Mapping of module path to Python source text.

        Raises:
            AssertionError: If any module crosses the boundary by import or by
                vocabulary.
        """
        violations = self.violations(sources)
        if violations:
            report = "\n".join(violations)
            raise AssertionError(report)
