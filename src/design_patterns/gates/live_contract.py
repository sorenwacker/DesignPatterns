"""Live Contract Gate: assert that beliefs about an external system hold.

This is the one gate a mocked suite cannot be. A suite built on doubles verifies
the code against its own assumptions, and a wrong assumption is invisible from
the inside.

Two things make the pattern work. The gate asserts what was observed rather than
what would be preferred, including where the observation is of a defect: that
turns the gate into a notification, failing on the day the behaviour is fixed
with a message saying what to do about it. And it exercises the project's own
client rather than a hand-rolled request, so a defect in the client surfaces too.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ObservedBehaviour:
    """What an external system was measured to do, and what to do when it changes.

    Attributes:
        name: What was measured, phrased so the failure report reads clearly.
        observed: The value the system actually returned.
        observed_on: Date of the observation in YYMMDD format.
        instruction: The action to take when the behaviour changes.

    Example:
        ```python
        record = ObservedBehaviour(
            name="assay sample types after an API-created assay",
            observed=[],
            observed_on="260806",
            instruction="The server now returns sample types; revisit the importer.",
        )
        ```
    """

    name: str
    observed: Any
    observed_on: str
    instruction: str

    def message(self, current: Any) -> str:
        """Build the failure text for a change in external behaviour.

        Args:
            current: The value the system returns now.

        Returns:
            str: Text contrasting the recorded value with the current one and
                stating the action the change calls for.
        """
        return (
            f"{self.name} returned {self.observed!r} on {self.observed_on} and "
            f"now returns {current!r}. {self.instruction}"
        )


class LiveContractGate:
    """Compares recorded external behaviour against a live instance.

    Example:
        ```python
        gate = LiveContractGate(
            os.environ.get("CONTRACT_URL"), os.environ.get("CONTRACT_TOKEN")
        )
        pytestmark = pytest.mark.skipif(not gate.configured, reason=gate.skip_reason())
        ```
    """

    def __init__(
        self,
        url: str | None,
        token: str | None,
        url_variable: str = "CONTRACT_URL",
        token_variable: str = "CONTRACT_TOKEN",
    ) -> None:
        """Point the gate at an instance, if one was supplied.

        Args:
            url: Base URL of the instance, typically from the environment.
            token: Credential for that instance, typically from the environment.
            url_variable: Name of the environment variable the caller reads
                ``url`` from, quoted in the skip reason.
            token_variable: Name of the environment variable the caller reads
                ``token`` from, quoted in the skip reason.
        """
        self._url = url
        self._token = token
        self._url_variable = url_variable
        self._token_variable = token_variable

    @property
    def configured(self) -> bool:
        """Whether an instance is available to run against.

        An unset environment variable often arrives as an empty string, which
        counts as absent.
        """
        return bool(self._url) and bool(self._token)

    def skip_reason(self) -> str:
        """Explain why the gate is inactive.

        Returns:
            str: Text naming the variables that activate the gate, so a skipped
                run says how to become a real one.
        """
        return (
            f"set {self._url_variable} and {self._token_variable} to run "
            f"against an instance"
        )

    def check(self, recorded: ObservedBehaviour, current: Any) -> None:
        """Assert that the system still behaves as recorded.

        Args:
            recorded: The observation this gate defends.
            current: The value read from the live instance, obtained through the
                project's own client rather than a hand-rolled request.

        Raises:
            AssertionError: If the current value differs from the recorded one.
                The message carries the instruction for what the change means.
        """
        if current != recorded.observed:
            raise AssertionError(recorded.message(current))
