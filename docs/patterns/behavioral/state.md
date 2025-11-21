# State Pattern

**Category:** Behavioral Pattern

## Intent

Allow an object to alter its behavior when its internal state changes. The object will appear to change its class. The State pattern encapsulates state-specific behavior into separate state objects and delegates state-dependent behavior to the current state object.

## Problem

When an object's behavior depends on its state and must change at runtime, conditional logic leads to:

- Complex conditional statements throughout the code
- Difficulty adding new states
- State-specific behavior scattered across methods
- Hard to understand state transitions
- Violation of single responsibility principle
- Rigid and inflexible state management

## When to Use

Use the State pattern when:

- **State-dependent behavior**: Object behavior changes based on internal state
- **Complex conditionals**: Multiple conditional statements based on state
- **State transitions**: Clear state transitions exist
- **State encapsulation**: Want to encapsulate state-specific behavior
- **Extensibility**: Need to add new states easily
- **State machines**: Implementing finite state machines

## When NOT to Use

Avoid the State pattern when:

- **Few states**: Object has only 2-3 simple states
- **No state transitions**: States don't change or transitions are trivial
- **Simple behavior**: State-dependent behavior is minimal
- **Overkill**: Pattern adds unnecessary complexity
- **Performance critical**: State object overhead is unacceptable

## Structure

The State pattern involves:

- **Context**: Maintains instance of concrete state representing current state
- **State**: Interface defining state-specific behavior
- **Concrete States**: Implement behavior for specific states
- **State Transitions**: States trigger transitions to other states

## Implementation

### Document Workflow Example

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
    def reject(self, document: Document) -> str:
        """Attempt to reject the document."""
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

    def reject(self, document: Document) -> str:
        """Cannot reject a draft."""
        return "Cannot reject a draft document"

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

    def reject(self, document: Document) -> str:
        """Reject and return to draft."""
        document.set_state(DraftState())
        return "Document rejected, returned to draft"

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

    def reject(self, document: Document) -> str:
        """Unpublish and return to draft."""
        document.set_state(DraftState())
        return "Document unpublished, returned to draft"

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

    def reject(self) -> str:
        """Reject the document."""
        return self._state.reject(self)

    def get_status(self) -> str:
        """Get current document status."""
        return self._state.get_status()
```

### Traffic Light Example

```python
class TrafficLightState(ABC):
    """Abstract base class for traffic light states."""

    @abstractmethod
    def next(self, light: TrafficLight) -> str:
        """Move to next state."""
        pass

    @abstractmethod
    def get_color(self) -> str:
        """Get the color of this state."""
        pass

class RedLightState(TrafficLightState):
    """Red light state."""

    def next(self, light: TrafficLight) -> str:
        """Change to green."""
        light.set_state(GreenLightState())
        return "Changed from Red to Green"

    def get_color(self) -> str:
        """Get color."""
        return "Red"

class GreenLightState(TrafficLightState):
    """Green light state."""

    def next(self, light: TrafficLight) -> str:
        """Change to yellow."""
        light.set_state(YellowLightState())
        return "Changed from Green to Yellow"

    def get_color(self) -> str:
        """Get color."""
        return "Green"

class YellowLightState(TrafficLightState):
    """Yellow light state."""

    def next(self, light: TrafficLight) -> str:
        """Change to red."""
        light.set_state(RedLightState())
        return "Changed from Yellow to Red"

    def get_color(self) -> str:
        """Get color."""
        return "Yellow"

class TrafficLight:
    """Context for traffic light states."""

    def __init__(self) -> None:
        """Initialize traffic light in red state."""
        self._state: TrafficLightState = RedLightState()

    def set_state(self, state: TrafficLightState) -> None:
        """Set the current state."""
        self._state = state

    def next(self) -> str:
        """Move to next state."""
        return self._state.next(self)

    def get_color(self) -> str:
        """Get current light color."""
        return self._state.get_color()
```

## Usage Example

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

# Traffic light
light = TrafficLight()
print(light.get_color())  # Red

print(light.next())  # Changed from Red to Green
print(light.get_color())  # Green

print(light.next())  # Changed from Green to Yellow
print(light.get_color())  # Yellow

print(light.next())  # Changed from Yellow to Red
print(light.get_color())  # Red
```

## Key Benefits

1. **Encapsulation**: State-specific behavior is encapsulated in state classes
2. **Single Responsibility**: Each state class has single responsibility
3. **Open/Closed Principle**: Easy to add new states without modifying context
4. **Eliminates conditionals**: Replaces complex conditional logic
5. **Explicit transitions**: State transitions are explicit and clear
6. **Maintainability**: State logic is organized and maintainable

## Drawbacks

1. **Increased classes**: Creates many state classes
2. **Complexity**: Can be overkill for simple state machines
3. **State sharing**: Sharing state between objects can be tricky
4. **Transition management**: Managing transitions can become complex
5. **Overhead**: State object creation and switching adds overhead

## Real-World Examples

- **Document workflows**: Draft, review, published states
- **TCP connections**: Closed, listening, established states
- **Vending machines**: Idle, coin inserted, dispensing states
- **Game characters**: Idle, walking, running, jumping states
- **Order processing**: Pending, confirmed, shipped, delivered states
- **Media players**: Playing, paused, stopped states
- **Authentication**: Logged out, authenticated, expired states

## Related Patterns

- **Strategy**: Similar structure but different intent (State changes behavior, Strategy selects algorithm)
- **Singleton**: State objects are often singletons
- **Flyweight**: Can share state objects across contexts
- **Memento**: Can save and restore states

## API Reference

::: design_patterns.behavioral.state
    options:
      show_root_heading: true
      show_source: true
