# Memento Pattern

**Category:** Behavioral Pattern

## Intent

Capture and externalize an object's internal state without violating encapsulation, so that the object can be restored to this state later. The Memento pattern is useful for implementing undo/redo functionality, checkpoints, and snapshots while preserving object encapsulation.

## Problem

When you need to save and restore object states, direct access to internal state leads to:

- Violating encapsulation by exposing internal structure
- Difficulty implementing undo/redo operations
- No way to save snapshots without exposing internals
- Tight coupling between state management and business logic
- Objects unable to save and restore their own state

## When to Use

Use the Memento pattern when:

- **Undo/redo**: Need to implement undo and redo functionality
- **Snapshots**: Want to save object state at specific points in time
- **State rollback**: Need to rollback to previous states
- **Transaction**: Implementing transactional behavior
- **Checkpoints**: Creating save points in games or applications
- **Preserve encapsulation**: State must be saved without exposing internals
- **State history**: Need to maintain history of state changes

## When NOT to Use

Avoid the Memento pattern when:

- **Simple state**: State is simple and can be easily recreated
- **Memory constraints**: Storing many mementos consumes too much memory
- **Public state**: All state is already public
- **No restoration needed**: Never need to restore previous states
- **Frequent changes**: State changes very frequently, making storage expensive
- **Serialization sufficient**: Simple serialization meets requirements

## Structure

The Memento pattern involves:

- **Originator**: Creates memento containing snapshot of its state
- **Memento**: Stores internal state of originator
- **Caretaker**: Manages mementos without examining their contents
- **State**: Internal state being saved and restored

## Implementation

### Text Editor Example

```python
from __future__ import annotations

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
        """Save current editor state."""
        self._mementos.append(editor.save())

    def undo(self, editor: TextEditor) -> bool:
        """Undo to previous state."""
        if len(self._mementos) <= 1:
            if self._mementos:
                self._mementos.pop()
                editor.restore(Memento(""))  # Restore to empty
                return True
            return False

        self._mementos.pop()  # Remove most recent state
        editor.restore(self._mementos[-1])  # Restore to previous state

        return True

    def get_history_size(self) -> int:
        """Get number of saved states."""
        return len(self._mementos)
```

### Game State Example

```python
class GameState:
    """Represents game state for checkpoint system."""

    def __init__(self) -> None:
        """Initialize game state."""
        self.level: int = 1
        self.score: int = 0
        self.lives: int = 3
        self.position: tuple[int, int] = (0, 0)

    def advance_level(self) -> None:
        """Advance to next level."""
        self.level += 1

    def add_score(self, points: int) -> None:
        """Add points to score."""
        self.score += points

    def lose_life(self) -> None:
        """Lose a life."""
        self.lives = max(0, self.lives - 1)

    def set_position(self, x: int, y: int) -> None:
        """Set player position."""
        self.position = (x, y)

    def save_checkpoint(self) -> GameMemento:
        """Create a checkpoint."""
        return GameMemento(
            level=self.level,
            score=self.score,
            lives=self.lives,
            position=self.position
        )

    def load_checkpoint(self, memento: GameMemento) -> None:
        """Load from checkpoint."""
        state = memento.get_state()
        self.level = state["level"]
        self.score = state["score"]
        self.lives = state["lives"]
        self.position = state["position"]

class GameMemento:
    """Memento for game state."""

    def __init__(
        self,
        level: int,
        score: int,
        lives: int,
        position: tuple[int, int]
    ) -> None:
        """Initialize game memento."""
        self._state = {
            "level": level,
            "score": score,
            "lives": lives,
            "position": position
        }

    def get_state(self) -> dict[str, Any]:
        """Get saved game state."""
        return self._state.copy()

class CheckpointManager:
    """Manages game checkpoints."""

    def __init__(self) -> None:
        """Initialize checkpoint manager."""
        self._checkpoints: list[GameMemento] = []

    def save_checkpoint(self, game: GameState) -> None:
        """Save a checkpoint."""
        self._checkpoints.append(game.save_checkpoint())

    def load_checkpoint(self, game: GameState, index: int = -1) -> bool:
        """Load a checkpoint."""
        if not self._checkpoints:
            return False

        if -len(self._checkpoints) <= index < len(self._checkpoints):
            game.load_checkpoint(self._checkpoints[index])
            return True

        return False

    def get_checkpoint_count(self) -> int:
        """Get number of saved checkpoints."""
        return len(self._checkpoints)

    def clear_checkpoints(self) -> None:
        """Clear all checkpoints."""
        self._checkpoints.clear()
```

## Usage Example

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

# Game checkpoints
game = GameState()
checkpoint_mgr = CheckpointManager()

# Save initial state
checkpoint_mgr.save_checkpoint(game)

# Play game
game.advance_level()
game.add_score(100)
game.set_position(10, 20)

# Save checkpoint
checkpoint_mgr.save_checkpoint(game)

# Continue playing
game.advance_level()
game.add_score(50)
game.lose_life()

print(f"Current: Level {game.level}, Score {game.score}, Lives {game.lives}")

# Load previous checkpoint
checkpoint_mgr.load_checkpoint(game, -1)
print(f"After load: Level {game.level}, Score {game.score}, Lives {game.lives}")
```

## Key Benefits

1. **Encapsulation preserved**: Internal state saved without exposing structure
2. **Simplified originator**: Originator doesn't manage its own history
3. **Undo/redo support**: Easy to implement undo and redo operations
4. **Snapshots**: Can save multiple snapshots at different points
5. **Rollback**: Can rollback to any previous state
6. **Single Responsibility**: State management separated from business logic

## Drawbacks

1. **Memory consumption**: Storing many mementos uses significant memory
2. **Expensive creation**: Creating mementos can be expensive for large objects
3. **Caretaker overhead**: Caretaker must manage memento lifecycle
4. **State size**: Large state makes mementos expensive
5. **Serialization complexity**: Complex objects are hard to capture

## Real-World Examples

- **Text editors**: Undo/redo functionality
- **Version control**: Git commits and checkpoints
- **Database transactions**: Rollback and commit
- **Games**: Save points and quick saves
- **Graphics editors**: Undo history for image edits
- **Form wizards**: Navigating back through multi-step forms
- **Configuration management**: Rollback to previous configurations
- **Simulation**: Restoring simulation states

## Related Patterns

- **Command**: Can use Memento to store command execution state
- **Iterator**: Can use Memento to capture iterator state
- **Prototype**: Memento can be implemented using Prototype for cloning
- **Caretaker**: Often uses composite to manage memento trees

## API Reference

::: design_patterns.behavioral.memento
    options:
      show_root_heading: true
      show_source: true
