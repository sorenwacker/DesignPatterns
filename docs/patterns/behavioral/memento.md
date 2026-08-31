# Memento Pattern

**Category:** Behavioral Pattern

## Overview

Capture and externalize an object's internal state without violating encapsulation, so that the object can be restored to this state later. This pattern is useful for implementing undo/redo functionality, checkpoints, and snapshots while preserving object encapsulation.

## Usage Guidelines

**Use when:**

- Need to implement undo and redo functionality
- Want to save object state at specific points in time
- Need to rollback to previous states
- Creating save points in games or applications

**Avoid when:**

- State is simple and can be easily recreated
- Storing many mementos consumes too much memory
- All state is already public
- Never need to restore previous states

## Implementation

```python
from __future__ import annotations
from typing import Any

class Memento:
    """Stores the internal state of the Originator."""

    def __init__(self, state: Any) -> None:
        """Initialize memento with state."""
        self._state = state

    def get_state(self) -> Any:
        """Get the stored state."""
        return self._state

class TextEditor:
    """Originator class that creates and restores mementos."""

    def __init__(self) -> None:
        """Initialize text editor with empty content."""
        self._content: str = ""

    def write(self, text: str) -> None:
        """Add text to the editor."""
        self._content += text

    def get_content(self) -> str:
        """Get current content."""
        return self._content

    def save(self) -> Memento:
        """Create a memento with current state."""
        return Memento(self._content)

    def restore(self, memento: Memento) -> None:
        """Restore state from memento."""
        self._content = memento.get_state()

class History:
    """Caretaker that manages mementos."""

    def __init__(self) -> None:
        """Initialize empty history."""
        self._mementos: list[Memento] = []

    def save(self, editor: TextEditor) -> None:
        """Record a checkpoint of the editor's current content."""
        self._mementos.append(editor.save())

    def undo(self, editor: TextEditor) -> bool:
        """Restore the most recent checkpoint and discard it.

        Returns False when no checkpoint remains, leaving the editor as it is.
        """
        if not self._mementos:
            return False
        editor.restore(self._mementos.pop())
        return True
```

Call `save` before a change you may want to undo. Each `undo` returns the editor to the most recent checkpoint and consumes it, so a run of undos walks back through the checkpoints in reverse order.

### Usage

```python
# Text editor with undo
editor = TextEditor()
history = History()

editor.write("Hello ")
history.save(editor)

editor.write("World")
history.save(editor)

editor.write("!")
print(editor.get_content())  # "Hello World!"

history.undo(editor)
print(editor.get_content())  # "Hello World"

history.undo(editor)
print(editor.get_content())  # "Hello "
```

## Trade-offs

**Benefits:**

1. Encapsulation preserved with internal state saved without exposing structure
2. Simplified originator that doesn't manage its own history
3. Easy to implement undo and redo operations
4. Can save multiple snapshots at different points

**Drawbacks:**

1. Storing many mementos uses significant memory
2. Creating mementos can be expensive for large objects
3. Caretaker must manage memento lifecycle
4. Large state makes mementos expensive

## Real-World Examples

- Text editors with undo/redo functionality
- Version control systems like Git with commits and checkpoints
- Database transactions with rollback and commit
- Games with save points and quick saves

## Related Patterns

- Command
- Iterator
- Prototype
- Caretaker

## API Reference

::: design_patterns.behavioral.memento
    options:
      show_root_heading: true
      show_source: true
