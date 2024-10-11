"""
Command Pattern Module

This module implements the Command design pattern, which encapsulates 
a request as an object, thereby allowing for parameterization of clients 
with queues, requests, and operations. 

Example:
    To use the command pattern, create command objects and pass them 
    to a remote control. Then execute the commands:

    ```
    remote = RemoteControl()
    light_on = LightOnCommand()
    light_off = LightOffCommand()

    remote.add_command(light_on)
    remote.add_command(light_off)

    remote.execute_commands()
    ```
"""

from typing import List


class Command:
    """Base class for encapsulating a command."""
    
    def execute(self) -> None:
        """Execute the command."""
        pass


class LightOnCommand(Command):
    """Command to turn on the light."""

    def execute(self) -> None:
        """Turns on the light."""
        print("Light is on")


class LightOffCommand(Command):
    """Command to turn off the light."""

    def execute(self) -> None:
        """Turns off the light."""
        print("Light is off")


class RemoteControl:
    """Invoker class that holds and executes commands."""

    def __init__(self) -> None:
        """Initializes the remote control with an empty command list."""
        self.commands: List[Command] = []

    def add_command(self, command: Command) -> None:
        """
        Adds a command to the invoker's queue.

        Args:
            command (Command): The command to add.
        """
        self.commands.append(command)

    def execute_commands(self) -> None:
        """Executes all stored commands."""
        for command in self.commands:
            command.execute()
        self.commands.clear()
