# State Pattern

**Category:** Behavioral Pattern

## Overview

Allow an object to alter its behavior when its internal state changes, making the object appear to change its class. This pattern encapsulates state-specific behavior into separate state objects and delegates state-dependent behavior to the current state object.

## Usage Guidelines

**Use when:**

- Object behavior changes based on internal state
- Multiple conditional statements based on state exist
- Clear state transitions exist between states
- State-specific behavior should be encapsulated

**Avoid when:**

- Object has only 2-3 simple states
- States don't change or transitions are trivial
- State-dependent behavior is minimal
- Pattern adds unnecessary complexity

## Implementation

```python
from __future__ import annotations
from abc import ABC, abstractmethod

class State(ABC):
    """Abstract base class for states."""

    @abstractmethod
    def publish(self, document: Document) -> str:
        """Attempt to publish the document."""
        pass

    @abstractmethod
    def approve(self, document: Document) -> str:
        """Attempt to approve the document."""
        pass

    @abstractmethod
    def get_status(self) -> str:
        """Get the current status name."""
        pass

class DraftState(State):
    """State representing a draft document."""

    def publish(self, document: Document) -> str:
        """Move document to moderation."""
        document.set_state(ModerationState())
        return "Document sent for moderation"

    def approve(self, document: Document) -> str:
        """Cannot approve a draft."""
        return "Cannot approve a draft document"

    def get_status(self) -> str:
        """Get status name."""
        return "Draft"

class ModerationState(State):
    """State representing a document under moderation."""

    def publish(self, document: Document) -> str:
        """Already in moderation."""
        return "Document is already in moderation"

    def approve(self, document: Document) -> str:
        """Approve and publish the document."""
        document.set_state(PublishedState())
        return "Document approved and published"

    def get_status(self) -> str:
        """Get status name."""
        return "Moderation"

class PublishedState(State):
    """State representing a published document."""

    def publish(self, document: Document) -> str:
        """Already published."""
        return "Document is already published"

    def approve(self, document: Document) -> str:
        """Already published."""
        return "Document is already published"

    def get_status(self) -> str:
        """Get status name."""
        return "Published"

class Document:
    """Context class that maintains a state and delegates behavior to it."""

    def __init__(self) -> None:
        """Initialize document in draft state."""
        self._state: State = DraftState()

    def set_state(self, state: State) -> None:
        """Set the current state."""
        self._state = state

    def publish(self) -> str:
        """Publish the document."""
        return self._state.publish(self)

    def approve(self) -> str:
        """Approve the document."""
        return self._state.approve(self)

    def get_status(self) -> str:
        """Get current document status."""
        return self._state.get_status()
```

### Usage

```python
# Document workflow
doc = Document()
print(doc.get_status())  # Draft

result = doc.publish()
print(result)  # Document sent for moderation
print(doc.get_status())  # Moderation

result = doc.approve()
print(result)  # Document approved and published
print(doc.get_status())  # Published
```

## Trade-offs

**Benefits:**

1. State-specific behavior is encapsulated in state classes
2. Each state class has single responsibility
3. Easy to add new states without modifying context (Open/Closed Principle)
4. Eliminates complex conditional logic

**Drawbacks:**

1. Creates many state classes increasing code volume
2. Can be overkill for simple state machines
3. Managing transitions can become complex
4. State object creation and switching adds overhead

## Real-World Examples

- Document workflows with draft, review, published states
- TCP connections with closed, listening, established states
- Vending machines with idle, coin inserted, dispensing states
- Order processing with pending, confirmed, shipped states

## Related Patterns

- Strategy
- Singleton
- Flyweight
- Memento

## API Reference

::: design_patterns.behavioral.state
    options:
      show_root_heading: true
      show_source: true
