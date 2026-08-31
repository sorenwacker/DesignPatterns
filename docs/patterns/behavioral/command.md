# Command Pattern

**Category:** Behavioral Pattern

## Overview

Encapsulate a request as an object, thereby allowing for parameterization of clients with queues, requests, and operations. This pattern supports undoable operations, request logging, and transaction management by turning requests into stand-alone objects.

## Usage Guidelines

**Use when:**

- Need to parameterize objects with operations
- Operations need to be queued for later execution
- Need to support undoable operations
- Operations must be logged for audit or recovery

**Avoid when:**

- Direct method calls are sufficient for simple operations
- No need for undo, logging, or queueing
- Command object overhead is unacceptable for performance
- Only one type of operation exists

## Implementation

```python
from __future__ import annotations

from abc import ABC, abstractmethod


class Light:
    """Receiver: the object a command acts on."""

    def __init__(self) -> None:
        self.is_on = False

    def turn_on(self) -> str:
        self.is_on = True
        return "Light is on"

    def turn_off(self) -> str:
        self.is_on = False
        return "Light is off"


class Command(ABC):
    """Interface every command implements: do the action, and reverse it."""

    @abstractmethod
    def execute(self) -> str:
        """Perform the action and describe what happened."""

    @abstractmethod
    def undo(self) -> str:
        """Reverse the action and describe what happened."""


class LightOnCommand(Command):
    """Command to turn a light on; undo turns it off again."""

    def __init__(self, light: Light) -> None:
        self._light = light

    def execute(self) -> str:
        return self._light.turn_on()

    def undo(self) -> str:
        return self._light.turn_off()


class LightOffCommand(Command):
    """Command to turn a light off; undo turns it on again."""

    def __init__(self, light: Light) -> None:
        self._light = light

    def execute(self) -> str:
        return self._light.turn_off()

    def undo(self) -> str:
        return self._light.turn_on()


class RemoteControl:
    """Invoker: queues commands, runs them, and can undo the last one run."""

    def __init__(self) -> None:
        self.commands: list[Command] = []
        self._history: list[Command] = []

    def add_command(self, command: Command) -> None:
        self.commands.append(command)

    def execute_commands(self) -> list[str]:
        results = [command.execute() for command in self.commands]
        self._history.extend(self.commands)
        self.commands.clear()
        return results

    def undo_last(self) -> str:
        if not self._history:
            return "Nothing to undo"
        return self._history.pop().undo()
```

### Usage

```python
light = Light()
remote = RemoteControl()

remote.add_command(LightOnCommand(light))
remote.add_command(LightOffCommand(light))
remote.add_command(LightOnCommand(light))

print(remote.execute_commands())  # ["Light is on", "Light is off", "Light is on"]
print(light.is_on)                # True

print(remote.undo_last())         # "Light is off"
print(light.is_on)                # False
print(remote.undo_last())         # "Light is on"
print(remote.undo_last())         # "Light is off"
print(remote.undo_last())         # "Nothing to undo"
```

The invoker never touches the light; it only knows that a command can be executed and undone. The receiver keeps the state, the command records how to change it and how to change it back, and the history in the invoker turns that into undo.

## Trade-offs

**Benefits:**

1. Decouples sender from receiver of requests
2. Easy to add new commands without changing existing code
3. Commands can be composed into macro commands
4. Supports undo and redo functionality

**Drawbacks:**

1. Creates many command classes increasing code volume
2. Adds complexity for simple operations
3. Storing commands consumes memory
4. Extra layer of indirection can impact performance

## Real-World Examples

- GUI buttons and menu items with each action as a command
- Text editors with undo/redo functionality
- Transaction systems with database transactions and rollback
- Job schedulers queueing jobs for execution

## Related Patterns

- Memento
- Prototype
- Composite
- Chain of Responsibility
- Strategy

## API Reference

::: design_patterns.behavioral.command
    options:
      show_root_heading: true
      show_source: true
