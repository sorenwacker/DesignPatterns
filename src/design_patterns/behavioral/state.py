"""State Pattern Module

The State pattern allows an object to alter its behavior when its internal state
changes. The object will appear to change its class. This pattern encapsulates
state-specific behavior into separate state objects and delegates state-dependent
behavior to the current state object.

Example:
    Document workflow with different states:

    ```python
    doc = Document()
    print(doc.get_status())  # "Draft"

    doc.publish()
    print(doc.get_status())  # "Moderation"

    doc.approve()
    print(doc.get_status())  # "Published"
    ```
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class State(ABC):
    """Abstract base class for states."""

    @abstractmethod
    def publish(self, document: Document) -> str:
        """Attempt to publish the document.

        Args:
            document: The document whose state is being managed.

        Returns:
            Result message.
        """

    @abstractmethod
    def approve(self, document: Document) -> str:
        """Attempt to approve the document.

        Args:
            document: The document whose state is being managed.

        Returns:
            Result message.
        """

    @abstractmethod
    def reject(self, document: Document) -> str:
        """Attempt to reject the document.

        Args:
            document: The document whose state is being managed.

        Returns:
            Result message.
        """

    @abstractmethod
    def get_status(self) -> str:
        """Get the current status name.

        Returns:
            Status string.
        """


class DraftState(State):
    """State representing a draft document."""

    def publish(self, document: Document) -> str:
        """Move document to moderation.

        Args:
            document: The document to publish.

        Returns:
            Success message.
        """
        document.set_state(ModerationState())
        return "Document sent for moderation"

    # `document` is part of the State interface; this state does not need it.
    def approve(self, document: Document) -> str:  # noqa: ARG002
        """Cannot approve a draft.

        Args:
            document: The document.

        Returns:
            Error message.
        """
        return "Cannot approve a draft document"

    # `document` is part of the State interface; this state does not need it.
    def reject(self, document: Document) -> str:  # noqa: ARG002
        """Cannot reject a draft.

        Args:
            document: The document.

        Returns:
            Error message.
        """
        return "Cannot reject a draft document"

    def get_status(self) -> str:
        """Get status name.

        Returns:
            Status string.
        """
        return "Draft"


class ModerationState(State):
    """State representing a document under moderation."""

    # `document` is part of the State interface; this state does not need it.
    def publish(self, document: Document) -> str:  # noqa: ARG002
        """Already in moderation.

        Args:
            document: The document.

        Returns:
            Info message.
        """
        return "Document is already in moderation"

    def approve(self, document: Document) -> str:
        """Approve and publish the document.

        Args:
            document: The document to approve.

        Returns:
            Success message.
        """
        document.set_state(PublishedState())
        return "Document approved and published"

    def reject(self, document: Document) -> str:
        """Reject and return to draft.

        Args:
            document: The document to reject.

        Returns:
            Success message.
        """
        document.set_state(DraftState())
        return "Document rejected, returned to draft"

    def get_status(self) -> str:
        """Get status name.

        Returns:
            Status string.
        """
        return "Moderation"


class PublishedState(State):
    """State representing a published document."""

    # `document` is part of the State interface; this state does not need it.
    def publish(self, document: Document) -> str:  # noqa: ARG002
        """Already published.

        Args:
            document: The document.

        Returns:
            Info message.
        """
        return "Document is already published"

    # `document` is part of the State interface; this state does not need it.
    def approve(self, document: Document) -> str:  # noqa: ARG002
        """Already published.

        Args:
            document: The document.

        Returns:
            Info message.
        """
        return "Document is already published"

    def reject(self, document: Document) -> str:
        """Unpublish and return to draft.

        Args:
            document: The document to unpublish.

        Returns:
            Success message.
        """
        document.set_state(DraftState())
        return "Document unpublished, returned to draft"

    def get_status(self) -> str:
        """Get status name.

        Returns:
            Status string.
        """
        return "Published"


class Document:
    """Context class that maintains a state and delegates behavior to it."""

    def __init__(self) -> None:
        """Initialize document in draft state."""
        self._state: State = DraftState()

    def set_state(self, state: State) -> None:
        """Set the current state.

        Args:
            state: The new state.
        """
        self._state = state

    def publish(self) -> str:
        """Publish the document.

        Returns:
            Result message from current state.
        """
        return self._state.publish(self)

    def approve(self) -> str:
        """Approve the document.

        Returns:
            Result message from current state.
        """
        return self._state.approve(self)

    def reject(self) -> str:
        """Reject the document.

        Returns:
            Result message from current state.
        """
        return self._state.reject(self)

    def get_status(self) -> str:
        """Get current document status.

        Returns:
            Current status string.
        """
        return self._state.get_status()


class TrafficLight:
    """Another example using traffic light states."""

    def __init__(self) -> None:
        """Initialize traffic light in red state."""
        self._state: TrafficLightState = RedLightState()

    def set_state(self, state: TrafficLightState) -> None:
        """Set the current state.

        Args:
            state: The new state.
        """
        self._state = state

    def next(self) -> str:
        """Move to next state.

        Returns:
            Result message.
        """
        return self._state.next(self)

    def get_color(self) -> str:
        """Get current light color.

        Returns:
            Color string.
        """
        return self._state.get_color()


class TrafficLightState(ABC):
    """Abstract base class for traffic light states."""

    @abstractmethod
    def next(self, light: TrafficLight) -> str:
        """Move to next state.

        Args:
            light: The traffic light.

        Returns:
            Result message.
        """

    @abstractmethod
    def get_color(self) -> str:
        """Get the color of this state.

        Returns:
            Color string.
        """


class RedLightState(TrafficLightState):
    """Red light state."""

    def next(self, light: TrafficLight) -> str:
        """Change to green.

        Args:
            light: The traffic light.

        Returns:
            Transition message.
        """
        light.set_state(GreenLightState())
        return "Changed from Red to Green"

    def get_color(self) -> str:
        """Get color.

        Returns:
            Red.
        """
        return "Red"


class GreenLightState(TrafficLightState):
    """Green light state."""

    def next(self, light: TrafficLight) -> str:
        """Change to yellow.

        Args:
            light: The traffic light.

        Returns:
            Transition message.
        """
        light.set_state(YellowLightState())
        return "Changed from Green to Yellow"

    def get_color(self) -> str:
        """Get color.

        Returns:
            Green.
        """
        return "Green"


class YellowLightState(TrafficLightState):
    """Yellow light state."""

    def next(self, light: TrafficLight) -> str:
        """Change to red.

        Args:
            light: The traffic light.

        Returns:
            Transition message.
        """
        light.set_state(RedLightState())
        return "Changed from Yellow to Red"

    def get_color(self) -> str:
        """Get color.

        Returns:
            Yellow.
        """
        return "Yellow"
