"""Tests for the Command pattern."""

from design_patterns.behavioral.command import (
    Command,
    LightOffCommand,
    LightOnCommand,
    RemoteControl,
)


def test_light_on_command_executes(capsys):
    """Test that LightOnCommand executes correctly."""
    command = LightOnCommand()
    command.execute()
    captured = capsys.readouterr()
    assert captured.out == "Light is on\n"


def test_light_off_command_executes(capsys):
    """Test that LightOffCommand executes correctly."""
    command = LightOffCommand()
    command.execute()
    captured = capsys.readouterr()
    assert captured.out == "Light is off\n"


def test_remote_control_adds_commands():
    """Test that RemoteControl can add commands."""
    remote = RemoteControl()
    light_on = LightOnCommand()
    remote.add_command(light_on)
    assert len(remote.commands) == 1


def test_remote_control_executes_commands(capsys):
    """Test that RemoteControl executes all commands."""
    remote = RemoteControl()
    remote.add_command(LightOnCommand())
    remote.add_command(LightOffCommand())

    remote.execute_commands()
    captured = capsys.readouterr()
    assert captured.out == "Light is on\nLight is off\n"


def test_remote_control_clears_commands_after_execution():
    """Test that RemoteControl clears commands after execution."""
    remote = RemoteControl()
    remote.add_command(LightOnCommand())
    remote.execute_commands()
    assert len(remote.commands) == 0


def test_remote_control_multiple_executions(capsys):
    """Test that RemoteControl can execute multiple batches of commands."""
    remote = RemoteControl()

    remote.add_command(LightOnCommand())
    remote.execute_commands()

    remote.add_command(LightOffCommand())
    remote.execute_commands()

    captured = capsys.readouterr()
    assert captured.out == "Light is on\nLight is off\n"
