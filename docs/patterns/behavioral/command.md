# Command Pattern

**Category:** Behavioral Pattern

## Intent

Encapsulate a request as an object, thereby allowing for parameterization of clients with queues, requests, and operations. The Command pattern supports undoable operations, request logging, and transaction management by turning requests into stand-alone objects.

## Problem

When operations need to be executed, queued, logged, or undone, direct method calls lead to:

- Tight coupling between requester and receiver
- Difficulty implementing undo/redo functionality
- No way to queue or log operations
- Hard to parameterize objects with operations
- Complex transaction management
- Inability to compose operations

## When to Use

Use the Command pattern when:

- **Parameterize objects**: Need to parameterize objects with operations
- **Queue operations**: Operations need to be queued for later execution
- **Undo/redo**: Need to support undoable operations
- **Logging**: Operations must be logged for audit or recovery
- **Transactions**: Implementing transaction-based systems
- **Macro recording**: Recording sequences of operations for playback
- **Decouple sender/receiver**: Sender and receiver of requests should be decoupled

## When NOT to Use

Avoid the Command pattern when:

- **Simple operations**: Direct method calls are sufficient
- **No history needed**: No need for undo, logging, or queueing
- **Performance critical**: Command object overhead is unacceptable
- **Single operation**: Only one type of operation exists
- **Immediate execution**: All operations execute immediately without queueing
- **Overkill**: Pattern adds unnecessary complexity

## Structure

The Command pattern involves:

- **Command**: Interface declaring execution method
- **Concrete Command**: Implements command and binds receiver with action
- **Client**: Creates concrete command and sets its receiver
- **Invoker**: Asks command to execute the request
- **Receiver**: Knows how to perform the operations

## Implementation

### Remote Control Example

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

## Usage Example

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

## Key Benefits

1. **Decoupling**: Decouples sender from receiver of requests
2. **Extensibility**: Easy to add new commands without changing existing code
3. **Composability**: Commands can be composed into macro commands
4. **Undo/Redo**: Supports undo and redo functionality
5. **Queueing**: Commands can be queued for delayed or remote execution
6. **Logging**: Operations can be logged for audit trails
7. **Transactions**: Can implement rollback by undoing commands
8. **Single Responsibility**: Separates operation invocation from execution

## Drawbacks

1. **Increased classes**: Creates many command classes
2. **Complexity**: Adds complexity for simple operations
3. **Memory overhead**: Storing commands consumes memory
4. **Indirection**: Extra layer of indirection can impact performance
5. **Command proliferation**: Many small command classes can be overwhelming

## Real-World Examples

- **GUI buttons and menu items**: Each button/menu action is a command
- **Text editors**: Undo/redo functionality
- **Transaction systems**: Database transactions and rollback
- **Macro recording**: Recording user actions for playback
- **Job schedulers**: Queuing jobs for execution
- **Remote procedure calls**: Executing operations on remote systems
- **Wizards**: Multi-step processes with undo capability
- **Game input**: Player actions as commands that can be replayed

## Related Patterns

- **Memento**: Can store command state for undo
- **Prototype**: Commands can be cloned for reuse
- **Composite**: Macro commands use composite pattern
- **Chain of Responsibility**: Commands can be chained
- **Strategy**: Command can use strategy for execution logic

## API Reference

::: design_patterns.behavioral.command
    options:
      show_root_heading: true
      show_source: true
