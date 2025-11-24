# Observer Pattern

**Category:** Behavioral Pattern

## Overview

Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically. This pattern is commonly used to implement distributed event handling systems and forms the basis for the model-view-controller (MVC) architectural pattern.

## Usage Guidelines

**Use when:**
- Object state changes need to trigger updates in other objects
- One object (subject) needs to notify many objects (observers)
- Subject and observers should be loosely coupled
- Set of observers can change at runtime

**Avoid when:**
- Direct method calls suffice for simple scenarios
- Notification overhead is unacceptable for performance
- Risk of memory leaks from forgotten observer references
- Specific notification order is critical

## Implementation

```python
from __future__ import annotations
from abc import ABC, abstractmethod

class Observer(ABC):
    """Abstract base class for observers."""

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """Receive update from subject.

        Args:
            subject: The subject that triggered the update.
        """
        pass

class Subject(ABC):
    """Abstract base class for subjects being observed."""

    def __init__(self) -> None:
        """Initialize an empty list of observers."""
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Attach an observer to the subject.

        Args:
            observer: The observer to attach.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Detach an observer from the subject.

        Args:
            observer: The observer to detach.
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self) -> None:
        """Notify all observers of a state change."""
        for observer in self._observers:
            observer.update(self)

class WeatherStation(Subject):
    """Concrete subject representing a weather station.

    Tracks weather data and notifies observers when it changes.
    """

    def __init__(self) -> None:
        """Initialize the weather station."""
        super().__init__()
        self._temperature: float = 0.0
        self._humidity: float = 0.0
        self._pressure: float = 0.0

    def set_measurements(
        self,
        temperature: float,
        humidity: float,
        pressure: float
    ) -> None:
        """Set weather measurements and notify observers.

        Args:
            temperature: Temperature in Celsius.
            humidity: Humidity percentage.
            pressure: Atmospheric pressure in hPa.
        """
        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure
        self.notify()

    def get_temperature(self) -> float:
        """Get current temperature."""
        return self._temperature

    def get_humidity(self) -> float:
        """Get current humidity."""
        return self._humidity

    def get_pressure(self) -> float:
        """Get current pressure."""
        return self._pressure

class PhoneDisplay(Observer):
    """Concrete observer that displays weather on a phone."""

    def __init__(self) -> None:
        """Initialize the phone display."""
        self._temperature: float = 0.0

    def update(self, subject: Subject) -> None:
        """Update display with new weather data.

        Args:
            subject: The weather station subject.
        """
        if isinstance(subject, WeatherStation):
            self._temperature = subject.get_temperature()

    def display(self) -> str:
        """Get display text."""
        return f"Phone Display: Temperature is {self._temperature}°C"
```

### Usage

```python
# Create weather station and displays
weather_station = WeatherStation()
phone_display = PhoneDisplay()

# Register observers
weather_station.attach(phone_display)

# Update weather data - all observers notified automatically
weather_station.set_measurements(25.5, 65, 1013)

print(phone_display.display())  # Phone Display: Temperature is 25.5°C

# Unregister an observer
weather_station.detach(phone_display)
```

## Trade-offs

**Benefits:**
1. Loose coupling between subject and observers
2. Can add/remove observers at runtime dynamically
3. One state change notifies multiple observers through broadcast
4. Add new observers without modifying subject (Open/Closed Principle)

**Drawbacks:**
1. Observers may be updated in unexpected order
2. Forgotten observer references can cause memory leaks
3. Notifying many observers can be slow
4. Notification chains can be hard to debug

## Real-World Examples

- GUI event systems for button clicks, mouse movements, keyboard events
- MVC frameworks where models notify views of data changes
- Stock market applications with price changes notifying multiple displays
- Social media feeds with new posts notifying followers

## Related Patterns

- Mediator
- Singleton
- Command
- State
- Pub-Sub

## API Reference

::: design_patterns.behavioral.observer
    options:
      show_root_heading: true
      show_source: true
