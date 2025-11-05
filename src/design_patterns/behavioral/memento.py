"""Memento Pattern Module

The Memento pattern captures and externalizes an object's internal state without
violating encapsulation, so that the object can be restored to this state later.
It's useful for implementing undo/redo functionality, checkpoints, and snapshots.

Example:
    Text editor with undo functionality:

    ```python
    editor = TextEditor()
    history = History()

    editor.write("Hello ")
    history.save(editor)

    editor.write("World!")
    history.save(editor)

    editor.write("!!!")

    history.undo(editor)  # Back to "Hello World!"
    history.undo(editor)  # Back to "Hello "
    ```
"""

from __future__ import annotations

from typing import Any


class Memento:
    """Stores the internal state of the Originator."""

    def __init__(self, state: Any) -> None:
        """Initialize memento with state.

        Args:
            state: State to store.
        """
        self._state = state

    def get_state(self) -> Any:
        """Get the stored state.

        Returns:
            The stored state.
        """
        return self._state


class TextEditor:
    """Originator class that creates and restores mementos."""

    def __init__(self) -> None:
        """Initialize text editor with empty content."""
        self._content: str = ""

    def write(self, text: str) -> None:
        """Add text to the editor.

        Args:
            text: Text to add.
        """
        self._content += text

    def get_content(self) -> str:
        """Get current content.

        Returns:
            Current content.
        """
        return self._content

    def save(self) -> Memento:
        """Create a memento with current state.

        Returns:
            Memento containing current state.
        """
        return Memento(self._content)

    def restore(self, memento: Memento) -> None:
        """Restore state from memento.

        Args:
            memento: Memento to restore from.
        """
        self._content = memento.get_state()


class History:
    """Caretaker that manages mementos."""

    def __init__(self) -> None:
        """Initialize empty history."""
        self._mementos: list[Memento] = []

    def save(self, editor: TextEditor) -> None:
        """Save current editor state.

        Args:
            editor: Editor to save.
        """
        self._mementos.append(editor.save())

    def undo(self, editor: TextEditor) -> bool:
        """Undo to previous state.

        Args:
            editor: Editor to restore.

        Returns:
            True if undo was successful, False if no history.
        """
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
        """Get number of saved states.

        Returns:
            Number of states in history.
        """
        return len(self._mementos)


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
        """Add points to score.

        Args:
            points: Points to add.
        """
        self.score += points

    def lose_life(self) -> None:
        """Lose a life."""
        self.lives = max(0, self.lives - 1)

    def set_position(self, x: int, y: int) -> None:
        """Set player position.

        Args:
            x: X coordinate.
            y: Y coordinate.
        """
        self.position = (x, y)

    def save_checkpoint(self) -> GameMemento:
        """Create a checkpoint.

        Returns:
            Memento with current game state.
        """
        return GameMemento(
            level=self.level,
            score=self.score,
            lives=self.lives,
            position=self.position
        )

    def load_checkpoint(self, memento: GameMemento) -> None:
        """Load from checkpoint.

        Args:
            memento: Checkpoint to load.
        """
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
        """Initialize game memento.

        Args:
            level: Current level.
            score: Current score.
            lives: Remaining lives.
            position: Player position.
        """
        self._state = {
            "level": level,
            "score": score,
            "lives": lives,
            "position": position
        }

    def get_state(self) -> dict[str, Any]:
        """Get saved game state.

        Returns:
            Dictionary containing game state.
        """
        return self._state.copy()


class CheckpointManager:
    """Manages game checkpoints."""

    def __init__(self) -> None:
        """Initialize checkpoint manager."""
        self._checkpoints: list[GameMemento] = []

    def save_checkpoint(self, game: GameState) -> None:
        """Save a checkpoint.

        Args:
            game: Game state to save.
        """
        self._checkpoints.append(game.save_checkpoint())

    def load_checkpoint(self, game: GameState, index: int = -1) -> bool:
        """Load a checkpoint.

        Args:
            game: Game state to restore.
            index: Checkpoint index (-1 for most recent).

        Returns:
            True if checkpoint was loaded successfully.
        """
        if not self._checkpoints:
            return False

        if -len(self._checkpoints) <= index < len(self._checkpoints):
            game.load_checkpoint(self._checkpoints[index])
            return True

        return False

    def get_checkpoint_count(self) -> int:
        """Get number of saved checkpoints.

        Returns:
            Number of checkpoints.
        """
        return len(self._checkpoints)

    def clear_checkpoints(self) -> None:
        """Clear all checkpoints."""
        self._checkpoints.clear()


class Configuration:
    """Configuration object with memento support."""

    def __init__(self) -> None:
        """Initialize configuration with defaults."""
        self.settings: dict[str, Any] = {
            "theme": "light",
            "language": "en",
            "auto_save": True,
            "font_size": 12
        }

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.

        Args:
            key: Setting key.
            value: Setting value.
        """
        self.settings[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: Setting key.
            default: Default value if key not found.

        Returns:
            Setting value or default.
        """
        return self.settings.get(key, default)

    def create_snapshot(self) -> ConfigMemento:
        """Create a snapshot of current configuration.

        Returns:
            Memento with current settings.
        """
        return ConfigMemento(self.settings.copy())

    def restore_snapshot(self, memento: ConfigMemento) -> None:
        """Restore configuration from snapshot.

        Args:
            memento: Snapshot to restore.
        """
        self.settings = memento.get_state()


class ConfigMemento:
    """Memento for configuration."""

    def __init__(self, settings: dict[str, Any]) -> None:
        """Initialize config memento.

        Args:
            settings: Settings to store.
        """
        self._settings = settings

    def get_state(self) -> dict[str, Any]:
        """Get stored settings.

        Returns:
            Copy of stored settings.
        """
        return self._settings.copy()
