"""Mediator Pattern Module

The Mediator pattern defines an object that encapsulates how a set of objects interact.
It promotes loose coupling by keeping objects from referring to each other explicitly
and lets you vary their interaction independently. The mediator centralizes complex
communications and control logic between related objects.

Example:
    Chat room where users communicate through mediator:

    ```python
    chatroom = ChatRoom()
    alice = User("Alice", chatroom)
    bob = User("Bob", chatroom)

    alice.send("Hi Bob!")  # Message sent through chatroom mediator
    bob.send("Hello Alice!")
    ```
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Mediator(ABC):
    """Abstract mediator interface."""

    @abstractmethod
    def send_message(self, message: str, sender: Colleague) -> None:
        """Send a message through the mediator.

        Args:
            message: Message to send.
            sender: Colleague sending the message.
        """


class Colleague(ABC):
    """Abstract colleague that communicates through mediator."""

    def __init__(self, mediator: Mediator) -> None:
        """Initialize colleague with a mediator.

        Args:
            mediator: The mediator to use for communication.
        """
        self.mediator = mediator

    @abstractmethod
    def receive(self, message: str) -> None:
        """Receive a message from the mediator.

        Args:
            message: Message received.
        """

    @abstractmethod
    def send(self, message: str) -> None:
        """Send a message through the mediator.

        Args:
            message: Message to send.
        """


class ChatRoom(Mediator):
    """Concrete mediator implementing a chat room."""

    def __init__(self) -> None:
        """Initialize chat room."""
        self.users: list[User] = []

    def register_user(self, user: User) -> None:
        """Register a user in the chat room.

        Args:
            user: User to register.
        """
        if user not in self.users:
            self.users.append(user)

    def send_message(self, message: str, sender: Colleague) -> None:
        """Send message to all users except sender.

        Args:
            message: Message to send.
            sender: User sending the message.
        """
        for user in self.users:
            if user != sender:
                user.receive(message)


class User(Colleague):
    """Concrete colleague representing a chat user."""

    def __init__(self, name: str, chatroom: ChatRoom) -> None:
        """Initialize user.

        Args:
            name: User name.
            chatroom: Chat room mediator.
        """
        super().__init__(chatroom)
        self.name = name
        self.messages: list[str] = []
        chatroom.register_user(self)

    def receive(self, message: str) -> None:
        """Receive a message.

        Args:
            message: Message received.
        """
        self.messages.append(f"Received: {message}")

    def send(self, message: str) -> None:
        """Send a message.

        Args:
            message: Message to send.
        """
        self.messages.append(f"Sent: {message}")
        self.mediator.send_message(message, self)

    def get_messages(self) -> list[str]:
        """Get all messages for this user.

        Returns:
            List of messages.
        """
        return self.messages


class AirTrafficControl(Mediator):
    """Mediator for coordinating aircraft."""

    def __init__(self) -> None:
        """Initialize air traffic control."""
        self.aircraft: list[Aircraft] = []

    def register_aircraft(self, aircraft: Aircraft) -> None:
        """Register an aircraft.

        Args:
            aircraft: Aircraft to register.
        """
        if aircraft not in self.aircraft:
            self.aircraft.append(aircraft)

    def send_message(self, message: str, sender: Colleague) -> None:
        """Broadcast message to all aircraft.

        Args:
            message: Message to broadcast.
            sender: Aircraft sending the message.
        """
        for aircraft in self.aircraft:
            if aircraft != sender:
                aircraft.receive(message)

    def request_landing(self, aircraft: Aircraft) -> str:
        """Handle landing request.

        Args:
            aircraft: Aircraft requesting landing.

        Returns:
            Landing permission status.
        """
        if isinstance(aircraft, Aircraft):
            return f"Landing clearance granted for {aircraft.call_sign}"
        return "Permission denied"


class Aircraft(Colleague):
    """Concrete colleague representing an aircraft."""

    def __init__(self, call_sign: str, atc: AirTrafficControl) -> None:
        """Initialize aircraft.

        Args:
            call_sign: Aircraft call sign.
            atc: Air traffic control mediator.
        """
        super().__init__(atc)
        self.call_sign = call_sign
        self.messages: list[str] = []
        atc.register_aircraft(self)

    def receive(self, message: str) -> None:
        """Receive a message from ATC.

        Args:
            message: Message received.
        """
        self.messages.append(f"[{self.call_sign}] Received: {message}")

    def send(self, message: str) -> None:
        """Send a message to ATC.

        Args:
            message: Message to send.
        """
        self.messages.append(f"[{self.call_sign}] Sent: {message}")
        self.mediator.send_message(f"{self.call_sign}: {message}", self)

    def request_landing(self) -> str:
        """Request landing permission.

        Returns:
            Landing permission response.
        """
        if isinstance(self.mediator, AirTrafficControl):
            return self.mediator.request_landing(self)
        return "No ATC available"


class SmartHome(Mediator):
    """Mediator for smart home devices."""

    def __init__(self) -> None:
        """Initialize smart home system."""
        self.devices: dict[str, SmartDevice] = {}
        self.events: list[str] = []

    def register_device(self, device: SmartDevice) -> None:
        """Register a smart device.

        Args:
            device: Device to register.
        """
        self.devices[device.name] = device

    def send_message(self, message: str, sender: Colleague) -> None:
        """Process device event.

        Args:
            message: Event message.
            sender: Device sending the event.
        """
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
        """Initialize smart device.

        Args:
            name: Device name.
            smart_home: Smart home mediator.
        """
        super().__init__(smart_home)
        self.name = name
        self.state: str = "off"
        self.notifications: list[str] = []
        smart_home.register_device(self)

    def receive(self, message: str) -> None:
        """Receive command from smart home.

        Args:
            message: Command received.
        """
        self.notifications.append(f"Command: {message}")

        if "turn on" in message.lower() or "activate" in message.lower():
            self.state = "on"
        elif "turn off" in message.lower() or "deactivate" in message.lower():
            self.state = "off"

    def send(self, message: str) -> None:
        """Send event to smart home.

        Args:
            message: Event message.
        """
        self.mediator.send_message(f"{self.name}: {message}", self)

    def trigger_event(self, event: str) -> None:
        """Trigger an event.

        Args:
            event: Event description.
        """
        self.send(event)
