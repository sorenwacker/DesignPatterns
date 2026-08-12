"""Observer Pattern Module

The Observer pattern defines a one-to-many dependency between objects so that when
one object changes state, all its dependents are notified and updated automatically.
This pattern is commonly used to implement distributed event handling systems and is
the basis for the model-view-controller (MVC) architectural pattern.

Example:
    Observing weather station data:

    ```python
    weather_station = WeatherStation()
    phone_display = PhoneDisplay()
    tv_display = TVDisplay()

    weather_station.attach(phone_display)
    weather_station.attach(tv_display)

    weather_station.set_temperature(25.5)  # Notifies all observers
    ```
"""

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


# Subclasses inherit attach/detach/notify; there is no step for them to supply.
class Subject(ABC):  # noqa: B024
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
        self, temperature: float, humidity: float, pressure: float
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
        """Get current temperature.

        Returns:
            Current temperature.
        """
        return self._temperature

    def get_humidity(self) -> float:
        """Get current humidity.

        Returns:
            Current humidity.
        """
        return self._humidity

    def get_pressure(self) -> float:
        """Get current pressure.

        Returns:
            Current pressure.
        """
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
        """Get display text.

        Returns:
            Current temperature display text.
        """
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
        """Get display text.

        Returns:
            Current weather display text.
        """
        return (
            f"TV Display: Temperature is {self._temperature}°C, "
            f"Humidity is {self._humidity}%"
        )


class NewsletterSubscriber(Observer):
    """Concrete observer representing a newsletter subscriber."""

    def __init__(self, email: str) -> None:
        """Initialize the subscriber.

        Args:
            email: Subscriber email address.
        """
        self.email = email
        self.messages: list[str] = []

    def update(self, subject: Subject) -> None:
        """Receive notification.

        Args:
            subject: The subject sending the notification.
        """
        if isinstance(subject, Newsletter):
            self.messages.append(subject.get_latest_article())


class Newsletter(Subject):
    """Concrete subject representing a newsletter.

    Notifies subscribers when new articles are published.
    """

    def __init__(self, name: str) -> None:
        """Initialize the newsletter.

        Args:
            name: Newsletter name.
        """
        super().__init__()
        self.name = name
        self._articles: list[str] = []

    def publish_article(self, article: str) -> None:
        """Publish a new article and notify subscribers.

        Args:
            article: The article content or title.
        """
        self._articles.append(article)
        self.notify()

    def get_latest_article(self) -> str:
        """Get the most recent article.

        Returns:
            The latest article.
        """
        return self._articles[-1] if self._articles else ""

    def get_article_count(self) -> int:
        """Get the total number of published articles.

        Returns:
            Number of articles.
        """
        return len(self._articles)
