"""Contract Gate: assert that a substitute matches what it substitutes for.

Test doubles drift from the real collaborator silently. A parameter is added to
the real client and not to the double, or an asynchronous method becomes
synchronous in the substitute. Both leave the suite green while every test runs
against an interface the production code no longer has.

The module also carries the example classes the documentation refers to: a real
client, a double that still corresponds to it, and a double that drifted in the
two ways this gate detects.
"""

import inspect
from collections.abc import Sequence
from typing import Any


class RealClient:
    """The collaborator a test double stands in for."""

    async def get(self, resource: str, identifier: int) -> dict[str, Any]:
        """Fetch one record.

        Args:
            resource: Collection name.
            identifier: Record identifier.

        Returns:
            dict[str, Any]: The stored record.
        """
        return {"resource": resource, "id": identifier}

    async def create(self, resource: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Create one record.

        Args:
            resource: Collection name.
            payload: Field values for the new record.

        Returns:
            dict[str, Any]: The created record.
        """
        return {"resource": resource, **payload}


class FaithfulDouble:
    """A stand-in whose signatures still correspond to RealClient."""

    async def get(self, resource: str, identifier: int) -> dict[str, Any]:
        """Return a canned record.

        Args:
            resource: Collection name.
            identifier: Record identifier.

        Returns:
            dict[str, Any]: A record built without a network call.
        """
        return {"resource": resource, "id": identifier}

    async def create(self, resource: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Record a creation without performing one.

        Args:
            resource: Collection name.
            payload: Field values for the new record.

        Returns:
            dict[str, Any]: The record that would have been created.
        """
        return {"resource": resource, **payload}


class DriftedDouble:
    """A stand-in that drifted in the two ways this gate detects.

    ``get`` stopped being a coroutine function and ``create`` renamed its second
    parameter. Both changes keep every existing assertion passing.
    """

    def get(self, resource: str, identifier: int) -> dict[str, Any]:
        """Return a canned record synchronously, unlike the real client.

        Args:
            resource: Collection name.
            identifier: Record identifier.

        Returns:
            dict[str, Any]: A record built without a network call.
        """
        return {"resource": resource, "id": identifier}

    async def create(self, resource: str, body: dict[str, Any]) -> dict[str, Any]:
        """Record a creation, naming its payload parameter differently.

        Args:
            resource: Collection name.
            body: Field values for the new record.

        Returns:
            dict[str, Any]: The record that would have been created.
        """
        return {"resource": resource, **body}


def signature_mismatches(
    real: type,
    substitute: type,
    covered: Sequence[str],
) -> list[str]:
    """Compare a substitute's methods against the real ones.

    Parameter names are compared rather than counts, because reordering and
    renaming pass a count check and break callers. Whether a method is a
    coroutine function is treated as part of its signature.

    Args:
        real: The class being stood in for.
        substitute: The stand-in to check.
        covered: Method names the substitute claims to provide.

    Returns:
        list[str]: One message per difference found, naming the method and
            the specific divergence.
    """
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
                f"{name}: {substitute.__name__} does not implement it; add it "
                f"or narrow the covered set."
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
        if real_async != inspect.iscoroutinefunction(fake_method):
            expected = "asynchronous" if real_async else "synchronous"
            problems.append(
                f"{name}: {real.__name__} is {expected} and "
                f"{substitute.__name__} is not."
            )
    return problems


class ContractGate:
    """Fails when a substitute has drifted from the real collaborator.

    Example:
        ```python
        ContractGate(RealClient, FaithfulDouble, ("get", "create")).check()
        ```
    """

    def __init__(self, real: type, substitute: type, covered: Sequence[str]) -> None:
        """Pair a substitute with the class it stands in for.

        Args:
            real: The class being stood in for.
            substitute: The stand-in to check.
            covered: Method names the substitute claims to provide.
        """
        self._real = real
        self._substitute = substitute
        self._covered = list(covered)

    def violations(self) -> list[str]:
        """Find every method that no longer corresponds.

        Returns:
            list[str]: One message per divergent method.
        """
        return signature_mismatches(self._real, self._substitute, self._covered)

    def check(self) -> None:
        """Assert that every covered method still corresponds.

        Raises:
            AssertionError: If any covered method diverges. The message
                describes each divergence separately.
        """
        violations = self.violations()
        if violations:
            report = "\n".join(violations)
            raise AssertionError(report)
