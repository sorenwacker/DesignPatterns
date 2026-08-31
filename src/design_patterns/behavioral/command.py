"""
Command Pattern Module

This module implements the Command design pattern, which encapsulates a
request as an object. A receiver (`Light`) holds the state, each command
records how to change it and how to change it back, and an invoker
(`RemoteControl`) queues commands, runs them, and can undo the last one run.

Example:
    ```
    light = Light()
    remote = RemoteControl()
    remote.add_command(LightOnCommand(light))
    remote.add_command(LightOffCommand(light))

    remote.execute_commands()  # ["Light is on", "Light is off"]
    remote.undo_last()  # "Light is on"
    ```
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Light:
    """Receiver: the object commands act on."""

    def __init__(self) -> None:
        """Start with the light off."""
        self.is_on = False

    def turn_on(self) -> str:
        """Turn the light on.

        Returns:
            str: A description of the new state.
        """
        self.is_on = True
        return "Light is on"

    def turn_off(self) -> str:
        """Turn the light off.

        Returns:
            str: A description of the new state.
        """
        self.is_on = False
        return "Light is off"


class Command(ABC):
    """Interface every command implements: do the action, and reverse it."""

    @abstractmethod
    def execute(self) -> str:
        """Perform the action.

        Returns:
            str: A description of what happened.
        """

    @abstractmethod
    def undo(self) -> str:
        """Reverse the action.

        Returns:
            str: A description of what happened.
        """


class LightOnCommand(Command):
    """Command to turn a light on; undo turns it off again."""

    def __init__(self, light: Light) -> None:
        """Bind the command to the light it controls.

        Args:
            light: The receiver.
        """
        self._light = light

    def execute(self) -> str:
        """Turn the light on.

        Returns:
            str: The receiver's description of its new state.
        """
        return self._light.turn_on()

    def undo(self) -> str:
        """Turn the light off again.

        Returns:
            str: The receiver's description of its new state.
        """
        return self._light.turn_off()


class LightOffCommand(Command):
    """Command to turn a light off; undo turns it on again."""

    def __init__(self, light: Light) -> None:
        """Bind the command to the light it controls.

        Args:
            light: The receiver.
        """
        self._light = light

    def execute(self) -> str:
        """Turn the light off.

        Returns:
            str: The receiver's description of its new state.
        """
        return self._light.turn_off()

    def undo(self) -> str:
        """Turn the light on again.

        Returns:
            str: The receiver's description of its new state.
        """
        return self._light.turn_on()


class RemoteControl:
    """Invoker: queues commands, runs them, and can undo the last one run."""

    def __init__(self) -> None:
        """Start with an empty queue and an empty history."""
        self.commands: list[Command] = []
        self._history: list[Command] = []

    def add_command(self, command: Command) -> None:
        """Queue a command for the next execution.

        Args:
            command: The command to add.
        """
        self.commands.append(command)

    def execute_commands(self) -> list[str]:
        """Run every queued command in order and remember it for undo.

        Returns:
            list[str]: Each command's description of what it did.
        """
        results = [command.execute() for command in self.commands]
        self._history.extend(self.commands)
        self.commands.clear()
        return results

    def undo_last(self) -> str:
        """Reverse the most recently executed command.

        Returns:
            str: The command's description of the reversal, or a message
                saying there was nothing to undo.
        """
        if not self._history:
            return "Nothing to undo"
        return self._history.pop().undo()
