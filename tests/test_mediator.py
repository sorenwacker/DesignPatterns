"""Tests for the Mediator pattern."""

from design_patterns.behavioral.mediator import (
    Aircraft,
    AirTrafficControl,
    ChatRoom,
    SmartDevice,
    SmartHome,
    User,
)


def test_chat_room_two_users():
    """Test chat room with two users."""
    chatroom = ChatRoom()
    alice = User("Alice", chatroom)
    bob = User("Bob", chatroom)

    alice.send("Hello Bob")

    assert "Sent: Hello Bob" in alice.get_messages()
    assert "Received: Hello Bob" in bob.get_messages()


def test_chat_room_multiple_users():
    """Test chat room with multiple users."""
    chatroom = ChatRoom()
    alice = User("Alice", chatroom)
    bob = User("Bob", chatroom)
    charlie = User("Charlie", chatroom)

    alice.send("Hello everyone")

    assert len(bob.get_messages()) == 1
    assert len(charlie.get_messages()) == 1
    assert len(alice.get_messages()) == 1  # Only sent message


def test_chat_room_sender_not_receiver():
    """Test that sender doesn't receive their own message."""
    chatroom = ChatRoom()
    alice = User("Alice", chatroom)
    User("Bob", chatroom)

    alice.send("Test message")

    alice_messages = alice.get_messages()
    assert all("Received" not in msg for msg in alice_messages if "Test message" in msg)


def test_chat_room_bidirectional():
    """Test bidirectional communication."""
    chatroom = ChatRoom()
    alice = User("Alice", chatroom)
    bob = User("Bob", chatroom)

    alice.send("Hi Bob")
    bob.send("Hi Alice")

    assert len(alice.get_messages()) == 2
    assert len(bob.get_messages()) == 2


def test_air_traffic_control():
    """Test air traffic control mediator."""
    atc = AirTrafficControl()
    flight1 = Aircraft("AA123", atc)
    flight2 = Aircraft("UA456", atc)

    flight1.send("Requesting landing clearance")

    assert len(flight2.messages) == 1
    assert "AA123" in flight2.messages[0]


def test_aircraft_landing_request():
    """Test aircraft landing request."""
    atc = AirTrafficControl()
    flight = Aircraft("BA789", atc)

    response = flight.request_landing()

    assert "Landing clearance granted" in response
    assert "BA789" in response


def test_multiple_aircraft():
    """Test multiple aircraft communication."""
    atc = AirTrafficControl()
    flight1 = Aircraft("AA123", atc)
    flight2 = Aircraft("UA456", atc)
    flight3 = Aircraft("BA789", atc)

    flight1.send("Weather update needed")

    assert len(flight2.messages) == 1
    assert len(flight3.messages) == 1


def test_smart_home_motion_sensor():
    """Test smart home motion detection."""
    smart_home = SmartHome()
    motion_sensor = SmartDevice("motion_sensor", smart_home)
    lights = SmartDevice("lights", smart_home)

    motion_sensor.send("motion detected")

    assert lights.state == "on"


def test_smart_home_door_sensor():
    """Test smart home door detection."""
    smart_home = SmartHome()
    door_sensor = SmartDevice("door_sensor", smart_home)
    alarm = SmartDevice("alarm", smart_home)

    door_sensor.send("door opened")

    assert alarm.state == "on"


def test_smart_home_multiple_devices():
    """Test smart home with multiple devices."""
    smart_home = SmartHome()
    motion_sensor = SmartDevice("motion_sensor", smart_home)
    lights = SmartDevice("lights", smart_home)
    alarm = SmartDevice("alarm", smart_home)

    assert lights.state == "off"
    assert alarm.state == "off"

    motion_sensor.send("motion detected")
    assert lights.state == "on"


def test_smart_device_notifications():
    """Test that smart devices receive notifications."""
    smart_home = SmartHome()
    device = SmartDevice("test_device", smart_home)

    device.receive("turn on")

    assert len(device.notifications) == 1
    assert "Command: turn on" in device.notifications


def test_smart_home_events_logged():
    """Test that smart home logs events."""
    smart_home = SmartHome()
    device = SmartDevice("sensor", smart_home)

    device.send("test event")

    assert len(smart_home.events) == 1
    assert "sensor: test event" in smart_home.events[0]


def test_mediator_decouples_objects():
    """Test that mediator decouples colleague objects."""
    chatroom = ChatRoom()
    alice = User("Alice", chatroom)
    bob = User("Bob", chatroom)

    # Alice doesn't need to know about Bob directly
    alice.send("Message")

    # But Bob still receives the message
    assert len(bob.get_messages()) == 1


def test_empty_chat_room():
    """Test sending message in empty chat room."""
    chatroom = ChatRoom()
    alice = User("Alice", chatroom)

    alice.send("Hello?")

    # Alice sent message but no one to receive it
    assert "Sent: Hello?" in alice.get_messages()


def test_device_state_changes():
    """Test smart device state changes."""
    smart_home = SmartHome()
    device = SmartDevice("light", smart_home)

    assert device.state == "off"

    device.receive("turn on")
    assert device.state == "on"

    device.receive("turn off")
    assert device.state == "off"
