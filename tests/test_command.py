"""Tests for the Command pattern."""

from design_patterns.behavioral.command import (
    Command,
    Light,
    LightOffCommand,
    LightOnCommand,
    RemoteControl,
)


def test_light_starts_off():
    """The receiver starts in the off state."""
    assert Light().is_on is False


def test_light_on_command_turns_the_light_on():
    """Executing the command changes the receiver and reports it."""
    light = Light()
    assert LightOnCommand(light).execute() == "Light is on"
    assert light.is_on is True


def test_light_off_command_turns_the_light_off():
    """Executing the command changes the receiver and reports it."""
    light = Light()
    light.turn_on()
    assert LightOffCommand(light).execute() == "Light is off"
    assert light.is_on is False


def test_undo_reverses_the_command():
    """Each command knows how to reverse its own effect."""
    light = Light()
    command = LightOnCommand(light)
    command.execute()
    assert command.undo() == "Light is off"
    assert light.is_on is False


def test_commands_share_the_interface():
    """Both concrete commands are Commands."""
    light = Light()
    assert isinstance(LightOnCommand(light), Command)
    assert isinstance(LightOffCommand(light), Command)


def test_remote_control_queues_commands():
    """Added commands wait in the queue until executed."""
    remote = RemoteControl()
    remote.add_command(LightOnCommand(Light()))
    assert len(remote.commands) == 1


def test_remote_control_executes_queued_commands_in_order():
    """Execution returns each command's result in queue order."""
    light = Light()
    remote = RemoteControl()
    remote.add_command(LightOnCommand(light))
    remote.add_command(LightOffCommand(light))

    assert remote.execute_commands() == ["Light is on", "Light is off"]
    assert light.is_on is False


def test_remote_control_clears_the_queue_after_execution():
    """A queue that stays full would re-run commands on the next call."""
    remote = RemoteControl()
    remote.add_command(LightOnCommand(Light()))
    remote.execute_commands()
    assert remote.commands == []
    assert remote.execute_commands() == []


def test_remote_control_undoes_the_last_executed_command():
    """Undo walks back through executed commands most recent first."""
    light = Light()
    remote = RemoteControl()
    remote.add_command(LightOnCommand(light))
    remote.add_command(LightOffCommand(light))
    remote.execute_commands()

    assert remote.undo_last() == "Light is on"
    assert light.is_on is True
    assert remote.undo_last() == "Light is off"
    assert light.is_on is False


def test_remote_control_reports_when_nothing_to_undo():
    """Undo on an empty history is a message, not an error."""
    assert RemoteControl().undo_last() == "Nothing to undo"
