# Mediator Pattern

**Category:** Behavioral Pattern

## Intent

Define an object that encapsulates how a set of objects interact. The Mediator pattern promotes loose coupling by keeping objects from referring to each other explicitly and lets you vary their interaction independently. The mediator centralizes complex communications and control logic between related objects.

## Problem

When objects need to communicate with each other, direct references lead to:

- Tight coupling between communicating objects
- Difficulty understanding object interactions
- Hard to modify interaction logic
- Objects knowing too much about each other
- Tangled dependencies making maintenance difficult
- Reusing components becomes challenging

## When to Use

Use the Mediator pattern when:

- **Complex communications**: Many objects communicate in complex ways
- **Centralized control**: Want to centralize communication logic
- **Loose coupling**: Objects shouldn't depend on each other directly
- **Reusability**: Want to reuse objects in different contexts
- **Interaction logic**: Communication logic is complex and should be separated
- **Difficult to understand**: Object relationships are hard to understand

## When NOT to Use

Avoid the Mediator pattern when:

- **Simple interactions**: Objects have simple, straightforward interactions
- **Performance critical**: Mediator indirection is unacceptable
- **Over-centralization**: Mediator becomes too complex (God object)
- **Direct communication**: Direct communication is clearer and simpler
- **Few objects**: Only 2-3 objects interact

## Structure

The Mediator pattern involves:

- **Mediator**: Interface defining communication methods
- **Concrete Mediator**: Implements coordination logic between colleagues
- **Colleague**: Interface for objects that communicate through mediator
- **Concrete Colleagues**: Implement colleague interface and communicate via mediator

## Implementation

### Chat Room Example

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

### Air Traffic Control Example

```python
class AirTrafficControl(Mediator):
    """Mediator for coordinating aircraft."""

    def __init__(self) -> None:
        """Initialize air traffic control."""
        self.aircraft: list[Aircraft] = []

    def register_aircraft(self, aircraft: Aircraft) -> None:
        """Register an aircraft."""
        if aircraft not in self.aircraft:
            self.aircraft.append(aircraft)

    def send_message(self, message: str, sender: Colleague) -> None:
        """Broadcast message to all aircraft."""
        for aircraft in self.aircraft:
            if aircraft != sender:
                aircraft.receive(message)

    def request_landing(self, aircraft: Aircraft) -> str:
        """Handle landing request."""
        if isinstance(aircraft, Aircraft):
            return f"Landing clearance granted for {aircraft.call_sign}"
        return "Permission denied"

class Aircraft(Colleague):
    """Concrete colleague representing an aircraft."""

    def __init__(self, call_sign: str, atc: AirTrafficControl) -> None:
        """Initialize aircraft."""
        super().__init__(atc)
        self.call_sign = call_sign
        self.messages: list[str] = []
        atc.register_aircraft(self)

    def receive(self, message: str) -> None:
        """Receive a message from ATC."""
        self.messages.append(f"[{self.call_sign}] Received: {message}")

    def send(self, message: str) -> None:
        """Send a message to ATC."""
        self.messages.append(f"[{self.call_sign}] Sent: {message}")
        self.mediator.send_message(f"{self.call_sign}: {message}", self)

    def request_landing(self) -> str:
        """Request landing permission."""
        if isinstance(self.mediator, AirTrafficControl):
            return self.mediator.request_landing(self)
        return "No ATC available"
```

### Smart Home Example

```python
class SmartHome(Mediator):
    """Mediator for smart home devices."""

    def __init__(self) -> None:
        """Initialize smart home system."""
        self.devices: dict[str, SmartDevice] = {}
        self.events: list[str] = []

    def register_device(self, device: SmartDevice) -> None:
        """Register a smart device."""
        self.devices[device.name] = device

    def send_message(self, message: str, sender: Colleague) -> None:
        """Process device event."""
        self.events.append(message)

        # Smart home logic based on events
        if "motion detected" in message.lower():
            # Turn on lights when motion detected
            if "lights" in self.devices:
                self.devices["lights"].receive("turn on")

        if "door opened" in message.lower():
            # Activate alarm when door opened
            if "alarm" in self.devices:
                self.devices["alarm"].receive("activate")

class SmartDevice(Colleague):
    """Concrete colleague representing a smart home device."""

    def __init__(self, name: str, smart_home: SmartHome) -> None:
        """Initialize smart device."""
        super().__init__(smart_home)
        self.name = name
        self.state: str = "off"
        self.notifications: list[str] = []
        smart_home.register_device(self)

    def receive(self, message: str) -> None:
        """Receive command from smart home."""
        self.notifications.append(f"Command: {message}")

        if "turn on" in message.lower() or "activate" in message.lower():
            self.state = "on"
        elif "turn off" in message.lower() or "deactivate" in message.lower():
            self.state = "off"

    def send(self, message: str) -> None:
        """Send event to smart home."""
        self.mediator.send_message(f"{self.name}: {message}", self)

    def trigger_event(self, event: str) -> None:
        """Trigger an event."""
        self.send(event)
```

## Usage Example

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

# Smart home
home = SmartHome()
motion_sensor = SmartDevice("motion_sensor", home)
lights = SmartDevice("lights", home)
alarm = SmartDevice("alarm", home)
door_sensor = SmartDevice("door_sensor", home)

# Trigger motion - lights turn on automatically
motion_sensor.trigger_event("motion detected")
print(lights.state)  # "on"

# Trigger door open - alarm activates automatically
door_sensor.trigger_event("door opened")
print(alarm.state)  # "on"
```

## Key Benefits

1. **Loose coupling**: Colleagues don't reference each other directly
2. **Centralized control**: Communication logic is in one place
3. **Simplified objects**: Colleagues are simpler, mediator handles complexity
4. **Easy to understand**: Interaction logic is centralized and clearer
5. **Reusability**: Colleagues can be reused with different mediators
6. **Flexible interactions**: Easy to change interaction logic

## Drawbacks

1. **God object**: Mediator can become too complex and hard to maintain
2. **Single point of failure**: Mediator failure affects all colleagues
3. **Indirect communication**: Can make debugging harder
4. **Performance**: Mediator adds indirection overhead
5. **Over-centralization**: Too much logic in mediator violates SRP

## Real-World Examples

- **GUI frameworks**: Dialog boxes coordinating widgets
- **Chat applications**: Chat rooms mediating user communications
- **Air traffic control**: Coordinating aircraft communications
- **MVC controllers**: Coordinating between models and views
- **Game engines**: Event managers coordinating game objects
- **Workflow systems**: Orchestrating task interactions
- **Message brokers**: RabbitMQ, Kafka coordinating producers/consumers

## Related Patterns

- **Observer**: Mediator uses Observer for notification
- **Facade**: Mediator centralizes complex interactions, Facade simplifies interface
- **Command**: Can use Command to encapsulate requests through mediator

## API Reference

::: design_patterns.behavioral.mediator
    options:
      show_root_heading: true
      show_source: true
