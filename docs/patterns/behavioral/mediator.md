# Mediator Pattern

**Category:** Behavioral Pattern

## Overview

Define an object that encapsulates how a set of objects interact. This pattern promotes loose coupling by keeping objects from referring to each other explicitly and lets you vary their interaction independently by centralizing complex communications and control logic.

## Usage Guidelines

**Use when:**

- Many objects communicate in complex ways
- Want to centralize communication logic
- Objects shouldn't depend on each other directly
- Want to reuse objects in different contexts

**Avoid when:**

- Objects have simple, straightforward interactions
- Mediator indirection is unacceptable for performance
- Mediator becomes too complex (God object)
- Direct communication is clearer and simpler

## Implementation

```python
from __future__ import annotations
from abc import ABC, abstractmethod

class Mediator(ABC):
    """Abstract mediator interface."""

    @abstractmethod
    def send_message(self, message: str, sender: Colleague) -> None:
        """Send a message through the mediator."""
        pass

class Colleague(ABC):
    """Abstract colleague that communicates through mediator."""

    def __init__(self, mediator: Mediator) -> None:
        """Initialize colleague with a mediator."""
        self.mediator = mediator

    @abstractmethod
    def receive(self, message: str) -> None:
        """Receive a message from the mediator."""
        pass

    @abstractmethod
    def send(self, message: str) -> None:
        """Send a message through the mediator."""
        pass

class ChatRoom(Mediator):
    """Concrete mediator implementing a chat room."""

    def __init__(self) -> None:
        """Initialize chat room."""
        self.users: list[User] = []

    def register_user(self, user: User) -> None:
        """Register a user in the chat room."""
        if user not in self.users:
            self.users.append(user)

    def send_message(self, message: str, sender: Colleague) -> None:
        """Send message to all users except sender."""
        for user in self.users:
            if user != sender:
                user.receive(message)

class User(Colleague):
    """Concrete colleague representing a chat user."""

    def __init__(self, name: str, chatroom: ChatRoom) -> None:
        """Initialize user."""
        super().__init__(chatroom)
        self.name = name
        self.messages: list[str] = []
        chatroom.register_user(self)

    def receive(self, message: str) -> None:
        """Receive a message."""
        self.messages.append(f"Received: {message}")

    def send(self, message: str) -> None:
        """Send a message."""
        self.messages.append(f"Sent: {message}")
        self.mediator.send_message(message, self)

    def get_messages(self) -> list[str]:
        """Get all messages for this user."""
        return self.messages
```

### Usage

```python
# Chat room
chatroom = ChatRoom()
alice = User("Alice", chatroom)
bob = User("Bob", chatroom)
charlie = User("Charlie", chatroom)

alice.send("Hello everyone!")
# Bob and Charlie receive the message

bob.send("Hi Alice!")
# Alice and Charlie receive the message

print(alice.get_messages())
print(bob.get_messages())
```

## Trade-offs

**Benefits:**

1. Loose coupling with colleagues not referencing each other directly
2. Centralized control of communication logic in one place
3. Simplified objects as mediator handles complexity
4. Colleagues can be reused with different mediators

**Drawbacks:**

1. Mediator can become too complex and hard to maintain (God object)
2. Single point of failure as mediator failure affects all colleagues
3. Indirect communication can make debugging harder
4. Mediator adds indirection overhead for performance

## Real-World Examples

- GUI frameworks with dialog boxes coordinating widgets
- Chat applications with chat rooms mediating communications
- Air traffic control coordinating aircraft
- MVC controllers coordinating models and views

## Related Patterns

- Observer
- Facade
- Command

## API Reference

::: design_patterns.behavioral.mediator
    options:
      show_root_heading: true
      show_source: true
