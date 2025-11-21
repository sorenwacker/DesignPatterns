# Observer Pattern

**Category:** Behavioral Pattern

## Intent

Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically. The Observer pattern is commonly used to implement distributed event handling systems and is the basis for the model-view-controller (MVC) architectural pattern.

## Problem

When objects need to be notified of state changes in other objects, direct coupling leads to:

- Tight coupling between the subject and its dependents
- Difficulty adding or removing dependents dynamically
- Subjects need to know about all their dependents
- Hard-coded notification logic
- Inflexible and rigid notification mechanisms
- Difficulty testing components in isolation

## When to Use

Use the Observer pattern when:

- **State change notifications**: Object state changes need to trigger updates in other objects
- **One-to-many relationships**: One object (subject) needs to notify many objects (observers)
- **Loose coupling desired**: Subject and observers should be loosely coupled
- **Dynamic relationships**: Set of observers can change at runtime
- **Event handling**: Implementing event-driven architectures
- **MVC architecture**: Model needs to notify views of changes
- **Publish-subscribe**: Implementing pub-sub messaging patterns

## When NOT to Use

Avoid the Observer pattern when:

- **Simple relationships**: Direct method calls suffice for simple scenarios
- **Performance critical**: Notification overhead is unacceptable
- **Memory leaks**: Risk of memory leaks from forgotten observer references
- **Guaranteed delivery**: Need guaranteed message delivery (use message queues instead)
- **Ordered notifications**: Specific notification order is critical
- **Complex dependencies**: Observer dependencies become too complex to manage

## Structure

The Observer pattern involves:

- **Subject**: Maintains list of observers and notifies them of state changes
- **Observer**: Interface for objects that should be notified
- **Concrete Subject**: Stores state and sends notifications when state changes
- **Concrete Observer**: Implements observer interface to receive notifications

## Implementation

### Weather Station Example

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

    def set_temperature(self, temperature: float) -> None:
        """Set temperature and notify observers.

        Args:
            temperature: Temperature in Celsius.
        """
        self._temperature = temperature
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
        self.update_count: int = 0

    def update(self, subject: Subject) -> None:
        """Update display with new weather data.

        Args:
            subject: The weather station subject.
        """
        if isinstance(subject, WeatherStation):
            self._temperature = subject.get_temperature()
            self.update_count += 1

    def display(self) -> str:
        """Get display text."""
        return f"Phone Display: Temperature is {self._temperature}°C"

class TVDisplay(Observer):
    """Concrete observer that displays weather on a TV."""

    def __init__(self) -> None:
        """Initialize the TV display."""
        self._temperature: float = 0.0
        self._humidity: float = 0.0
        self.update_count: int = 0

    def update(self, subject: Subject) -> None:
        """Update display with new weather data.

        Args:
            subject: The weather station subject.
        """
        if isinstance(subject, WeatherStation):
            self._temperature = subject.get_temperature()
            self._humidity = subject.get_humidity()
            self.update_count += 1

    def display(self) -> str:
        """Get display text."""
        return (f"TV Display: Temperature is {self._temperature}°C, "
                f"Humidity is {self._humidity}%")
```

### Newsletter Example

```python
class NewsletterSubscriber(Observer):
    """Concrete observer representing a newsletter subscriber."""

    def __init__(self, email: str) -> None:
        """Initialize the subscriber."""
        self.email = email
        self.messages: list[str] = []

    def update(self, subject: Subject) -> None:
        """Receive notification."""
        if isinstance(subject, Newsletter):
            self.messages.append(subject.get_latest_article())

class Newsletter(Subject):
    """Concrete subject representing a newsletter.

    Notifies subscribers when new articles are published.
    """

    def __init__(self, name: str) -> None:
        """Initialize the newsletter."""
        super().__init__()
        self.name = name
        self._articles: list[str] = []

    def publish_article(self, article: str) -> None:
        """Publish a new article and notify subscribers."""
        self._articles.append(article)
        self.notify()

    def get_latest_article(self) -> str:
        """Get the most recent article."""
        return self._articles[-1] if self._articles else ""

    def get_article_count(self) -> int:
        """Get the total number of published articles."""
        return len(self._articles)
```

## Usage Example

```python
# Create weather station and displays
weather_station = WeatherStation()
phone_display = PhoneDisplay()
tv_display = TVDisplay()

# Register observers
weather_station.attach(phone_display)
weather_station.attach(tv_display)

# Update weather data - all observers notified automatically
weather_station.set_measurements(25.5, 65, 1013)

print(phone_display.display())  # Phone Display: Temperature is 25.5°C
print(tv_display.display())  # TV Display: Temperature is 25.5°C, Humidity is 65%

# Update temperature only
weather_station.set_temperature(26.0)
print(phone_display.display())  # Phone Display: Temperature is 26.0°C

# Unregister an observer
weather_station.detach(tv_display)
weather_station.set_temperature(27.0)  # Only phone_display is notified

# Newsletter example
newsletter = Newsletter("Tech News")
subscriber1 = NewsletterSubscriber("user1@example.com")
subscriber2 = NewsletterSubscriber("user2@example.com")

newsletter.attach(subscriber1)
newsletter.attach(subscriber2)

newsletter.publish_article("New Python 3.12 Released")
print(len(subscriber1.messages))  # 1
print(len(subscriber2.messages))  # 1
```

## Key Benefits

1. **Loose coupling**: Subject and observers are loosely coupled
2. **Dynamic relationships**: Can add/remove observers at runtime
3. **Broadcast communication**: One state change notifies multiple observers
4. **Open/Closed Principle**: Add new observers without modifying subject
5. **Event-driven**: Natural fit for event-driven architectures
6. **MVC support**: Foundation for model-view-controller pattern
7. **Reusability**: Observers can be reused with different subjects

## Drawbacks

1. **Unexpected updates**: Observers may be updated in unexpected order
2. **Memory leaks**: Forgotten observer references can cause memory leaks
3. **Performance**: Notifying many observers can be slow
4. **Complexity**: Can become complex with many observers and subjects
5. **No guaranteed delivery**: No guarantee observers receive or process updates
6. **Update storms**: Cascading updates can cause performance issues
7. **Debugging**: Notification chains can be hard to debug

## Real-World Examples

- **GUI event systems**: Button clicks, mouse movements, keyboard events
- **MVC frameworks**: Model notifying views of data changes
- **Spreadsheets**: Cells updating when dependent cells change
- **Stock market applications**: Price changes notifying multiple displays
- **Social media feeds**: New posts notifying followers
- **Monitoring systems**: Sensors notifying dashboards and alerts
- **RSS readers**: News sources notifying subscribers of updates
- **Real-time dashboards**: Data sources notifying visualization components

## Related Patterns

- **Mediator**: Mediator centralizes communication, Observer distributes it
- **Singleton**: Subject is sometimes implemented as singleton
- **Command**: Commands can be used to implement undo/redo with observers
- **State**: State changes can trigger observer notifications
- **Pub-Sub**: Observer is the foundation for publish-subscribe systems

## API Reference

::: design_patterns.behavioral.observer
    options:
      show_root_heading: true
      show_source: true
