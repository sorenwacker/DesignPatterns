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
        """Adds a command to the invoker's queue.

        Args:
            command: The command to add.
        """
        self.commands.append(command)

    def execute_commands(self) -> None:
        """Executes all stored commands."""
        for command in self.commands:
            command.execute()
        self.commands.clear()
```

### Usage

```python
# Create remote control (invoker)
remote = RemoteControl()

# Create commands
light_on = LightOnCommand()
light_off = LightOffCommand()

# Add commands to remote
remote.add_command(light_on)
remote.add_command(light_off)
remote.add_command(light_on)

# Execute all commands
remote.execute_commands()
# Output:
# Light is on
# Light is off
# Light is on
```

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
