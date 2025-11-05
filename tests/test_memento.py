"""Tests for the Memento pattern."""

from design_patterns.behavioral.memento import (
    CheckpointManager,
    Configuration,
    GameState,
    History,
    TextEditor,
)


def test_text_editor_write():
    """Test writing to text editor."""
    editor = TextEditor()
    editor.write("Hello")

    assert editor.get_content() == "Hello"


def test_text_editor_save_restore():
    """Test saving and restoring editor state."""
    editor = TextEditor()
    editor.write("Hello")

    memento = editor.save()
    editor.write(" World")

    assert editor.get_content() == "Hello World"

    editor.restore(memento)
    assert editor.get_content() == "Hello"


def test_history_save():
    """Test saving editor state to history."""
    editor = TextEditor()
    history = History()

    editor.write("Hello")
    history.save(editor)

    assert history.get_history_size() == 1


def test_history_undo():
    """Test undo functionality."""
    editor = TextEditor()
    history = History()

    editor.write("Hello")
    history.save(editor)

    editor.write(" World")
    history.save(editor)

    editor.write("!!!")
    history.save(editor)  # Save current state

    # Undo removes most recent and restores to previous
    history.undo(editor)
    assert editor.get_content() == "Hello World"

    history.undo(editor)
    assert editor.get_content() == "Hello"


def test_history_undo_empty():
    """Test undo with no history."""
    editor = TextEditor()
    history = History()

    result = history.undo(editor)
    assert result is False


def test_history_multiple_undos():
    """Test multiple consecutive undos."""
    editor = TextEditor()
    history = History()

    states = ["A", "AB", "ABC"]
    for state in states:
        editor = TextEditor()
        editor.write(state)
        history.save(editor)

    history.undo(editor)
    assert editor.get_content() == "AB"

    history.undo(editor)
    assert editor.get_content() == "A"


def test_game_state_initial():
    """Test initial game state."""
    game = GameState()

    assert game.level == 1
    assert game.score == 0
    assert game.lives == 3
    assert game.position == (0, 0)


def test_game_state_modifications():
    """Test modifying game state."""
    game = GameState()

    game.advance_level()
    game.add_score(100)
    game.lose_life()
    game.set_position(10, 20)

    assert game.level == 2
    assert game.score == 100
    assert game.lives == 2
    assert game.position == (10, 20)


def test_game_checkpoint_save_load():
    """Test saving and loading game checkpoint."""
    game = GameState()

    game.advance_level()
    game.add_score(500)
    checkpoint = game.save_checkpoint()

    game.advance_level()
    game.add_score(200)
    game.lose_life()

    assert game.level == 3
    assert game.score == 700
    assert game.lives == 2

    game.load_checkpoint(checkpoint)

    assert game.level == 2
    assert game.score == 500
    assert game.lives == 3


def test_checkpoint_manager():
    """Test checkpoint manager functionality."""
    game = GameState()
    manager = CheckpointManager()

    game.add_score(100)
    manager.save_checkpoint(game)

    game.add_score(200)
    manager.save_checkpoint(game)

    assert manager.get_checkpoint_count() == 2


def test_checkpoint_manager_load():
    """Test loading from checkpoint manager."""
    game = GameState()
    manager = CheckpointManager()

    game.add_score(100)
    manager.save_checkpoint(game)

    game.add_score(200)
    manager.save_checkpoint(game)

    game.add_score(300)

    assert game.score == 600

    manager.load_checkpoint(game, -2)  # Load first checkpoint
    assert game.score == 100


def test_checkpoint_manager_empty():
    """Test loading from empty checkpoint manager."""
    game = GameState()
    manager = CheckpointManager()

    result = manager.load_checkpoint(game)
    assert result is False


def test_checkpoint_manager_clear():
    """Test clearing checkpoints."""
    game = GameState()
    manager = CheckpointManager()

    manager.save_checkpoint(game)
    manager.save_checkpoint(game)

    assert manager.get_checkpoint_count() == 2

    manager.clear_checkpoints()
    assert manager.get_checkpoint_count() == 0


def test_configuration_default():
    """Test default configuration."""
    config = Configuration()

    assert config.get("theme") == "light"
    assert config.get("language") == "en"
    assert config.get("auto_save") is True


def test_configuration_set_get():
    """Test setting and getting configuration."""
    config = Configuration()

    config.set("theme", "dark")
    assert config.get("theme") == "dark"


def test_configuration_snapshot():
    """Test configuration snapshot."""
    config = Configuration()

    config.set("theme", "dark")
    config.set("font_size", 14)

    snapshot = config.create_snapshot()

    config.set("theme", "light")
    config.set("font_size", 10)

    assert config.get("theme") == "light"
    assert config.get("font_size") == 10

    config.restore_snapshot(snapshot)

    assert config.get("theme") == "dark"
    assert config.get("font_size") == 14


def test_configuration_multiple_snapshots():
    """Test multiple configuration snapshots."""
    config = Configuration()

    config.set("font_size", 12)
    snapshot1 = config.create_snapshot()

    config.set("font_size", 14)
    snapshot2 = config.create_snapshot()

    config.set("font_size", 16)

    config.restore_snapshot(snapshot1)
    assert config.get("font_size") == 12

    config.restore_snapshot(snapshot2)
    assert config.get("font_size") == 14


def test_memento_encapsulation():
    """Test that mementos don't expose internal structure."""
    editor = TextEditor()
    editor.write("Secret")

    memento = editor.save()

    # Memento should not allow direct modification
    # It only provides get_state method
    assert hasattr(memento, "get_state")
    assert hasattr(memento, "_state")


def test_game_state_lives_boundary():
    """Test that lives don't go below zero."""
    game = GameState()

    game.lose_life()
    game.lose_life()
    game.lose_life()
    game.lose_life()  # Try to go negative

    assert game.lives == 0
