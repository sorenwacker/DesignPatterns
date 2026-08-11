"""Population Gate: assert that only one implementation of a kind exists.

The gate applies where duplication itself is the defect rather than any single
instance being wrong, most commonly a set of hand-written test doubles for one
collaborator. Detection works on structure rather than on names: a search for
``class _Fake`` finds the doubles named that way and misses the one called
``MockClient``, while a check on the method set finds both.
"""

import ast
from collections.abc import Mapping


class ClassShapeDetector:
    """Finds classes whose method set overlaps a reference set.

    Example:
        ```python
        detector = ClassShapeDetector({"get", "create", "delete"}, minimum_overlap=2)
        detector.matching_classes("class MockClient:\\n    def get(self): ...")
        ```
    """

    def __init__(self, methods: set[str], minimum_overlap: int = 2) -> None:
        """Configure the shape to look for.

        Args:
            methods: Method names characteristic of the real collaborator.
            minimum_overlap: How many of those methods a class must define
                before it counts as the same shape. Too low a value matches
                unrelated classes; too high a value misses partial copies.
        """
        self._methods = set(methods)
        self._minimum_overlap = minimum_overlap

    def matching_classes(self, source: str) -> list[str]:
        """Find classes in a source file that have the configured shape.

        Args:
            source: Python source text to parse.

        Returns:
            list[str]: Names of matching classes, in the order they appear.

        Raises:
            SyntaxError: If the source cannot be parsed.
        """
        matches = []
        for node in ast.walk(ast.parse(source)):
            if not isinstance(node, ast.ClassDef):
                continue
            defined = {
                item.name
                for item in node.body
                if isinstance(item, ast.FunctionDef | ast.AsyncFunctionDef)
            }
            if len(defined & self._methods) >= self._minimum_overlap:
                matches.append(node.name)
        return matches


class PopulationGate:
    """Fails when more than the sanctioned implementation has a given shape.

    Example:
        ```python
        gate = PopulationGate(detector, {"FakeClient"}, "tests/doubles.py")
        gate.check({"tests/test_import.py": source})
        ```
    """

    def __init__(
        self,
        detector: ClassShapeDetector,
        sanctioned: set[str],
        replacement: str,
    ) -> None:
        """Configure the permitted population.

        Args:
            detector: The shape detector identifying candidates.
            sanctioned: Class names allowed to have the shape.
            replacement: What offenders should use instead, named precisely
                enough to act on.
        """
        self._detector = detector
        self._sanctioned = set(sanctioned)
        self._replacement = replacement

    def violations(self, sources: Mapping[str, str]) -> list[str]:
        """Find every unsanctioned class with the configured shape.

        Args:
            sources: Mapping of file path to Python source text.

        Returns:
            list[str]: One message per offender, ordered by file path, naming
                the file, the class, and the sanctioned replacement.
        """
        return [
            f"{path}:{name} has the shape of the real collaborator; "
            f"use {self._replacement} instead."
            for path, source in sorted(sources.items())
            for name in self._detector.matching_classes(source)
            if name not in self._sanctioned
        ]

    def check(self, sources: Mapping[str, str]) -> None:
        """Assert that only the sanctioned implementation has the shape.

        Args:
            sources: Mapping of file path to Python source text.

        Raises:
            AssertionError: If any unsanctioned class matches. The message
                lists every offender rather than the first one.
        """
        violations = self.violations(sources)
        if violations:
            report = "\n".join(violations)
            raise AssertionError(report)
