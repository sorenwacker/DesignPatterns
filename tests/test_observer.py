"""Tests for the Observer pattern."""

from design_patterns.behavioral.observer import (
    Newsletter,
    NewsletterSubscriber,
    PhoneDisplay,
    TVDisplay,
    WeatherStation,
)


def test_weather_station_attach_observer():
    """Test attaching observers to weather station."""
    station = WeatherStation()
    phone = PhoneDisplay()

    station.attach(phone)
    assert phone in station._observers


def test_weather_station_detach_observer():
    """Test detaching observers from weather station."""
    station = WeatherStation()
    phone = PhoneDisplay()

    station.attach(phone)
    station.detach(phone)
    assert phone not in station._observers


def test_weather_station_notify_single_observer():
    """Test that observers receive notifications."""
    station = WeatherStation()
    phone = PhoneDisplay()

    station.attach(phone)
    station.set_temperature(25.0)

    assert phone._temperature == 25.0
    assert phone.update_count == 1


def test_weather_station_notify_multiple_observers():
    """Test that multiple observers receive notifications."""
    station = WeatherStation()
    phone = PhoneDisplay()
    tv = TVDisplay()

    station.attach(phone)
    station.attach(tv)
    station.set_temperature(22.5)

    assert phone._temperature == 22.5
    assert tv._temperature == 22.5
    assert phone.update_count == 1
    assert tv.update_count == 1


def test_weather_station_set_measurements():
    """Test setting all measurements at once."""
    station = WeatherStation()
    tv = TVDisplay()

    station.attach(tv)
    station.set_measurements(20.0, 65.0, 1013.25)

    assert tv._temperature == 20.0
    assert tv._humidity == 65.0
    assert tv.update_count == 1


def test_weather_station_multiple_updates():
    """Test multiple updates to observers."""
    station = WeatherStation()
    phone = PhoneDisplay()

    station.attach(phone)
    station.set_temperature(20.0)
    station.set_temperature(25.0)
    station.set_temperature(30.0)

    assert phone._temperature == 30.0
    assert phone.update_count == 3


def test_phone_display():
    """Test phone display shows correct information."""
    station = WeatherStation()
    phone = PhoneDisplay()

    station.attach(phone)
    station.set_temperature(18.5)

    assert phone.display() == "Phone Display: Temperature is 18.5°C"


def test_tv_display():
    """Test TV display shows correct information."""
    station = WeatherStation()
    tv = TVDisplay()

    station.attach(tv)
    station.set_measurements(22.0, 55.0, 1010.0)

    assert tv.display() == "TV Display: Temperature is 22.0°C, Humidity is 55.0%"


def test_observer_no_duplicate_attach():
    """Test that observers aren't added twice."""
    station = WeatherStation()
    phone = PhoneDisplay()

    station.attach(phone)
    station.attach(phone)

    assert len(station._observers) == 1


def test_detached_observer_no_update():
    """Test that detached observers don't receive updates."""
    station = WeatherStation()
    phone = PhoneDisplay()

    station.attach(phone)
    station.set_temperature(20.0)
    station.detach(phone)
    station.set_temperature(25.0)

    assert phone._temperature == 20.0
    assert phone.update_count == 1


def test_newsletter_subscriber():
    """Test newsletter subscription."""
    newsletter = Newsletter("Tech News")
    subscriber1 = NewsletterSubscriber("user1@example.com")
    subscriber2 = NewsletterSubscriber("user2@example.com")

    newsletter.attach(subscriber1)
    newsletter.attach(subscriber2)

    newsletter.publish_article("New Python Release")

    assert len(subscriber1.messages) == 1
    assert len(subscriber2.messages) == 1
    assert subscriber1.messages[0] == "New Python Release"


def test_newsletter_multiple_articles():
    """Test multiple article publications."""
    newsletter = Newsletter("Tech News")
    subscriber = NewsletterSubscriber("user@example.com")

    newsletter.attach(subscriber)
    newsletter.publish_article("Article 1")
    newsletter.publish_article("Article 2")
    newsletter.publish_article("Article 3")

    assert len(subscriber.messages) == 3
    assert subscriber.messages[0] == "Article 1"
    assert subscriber.messages[2] == "Article 3"


def test_newsletter_get_latest_article():
    """Test getting the latest article."""
    newsletter = Newsletter("Tech News")
    newsletter.publish_article("First Article")
    newsletter.publish_article("Second Article")

    assert newsletter.get_latest_article() == "Second Article"
    assert newsletter.get_article_count() == 2


def test_newsletter_empty():
    """Test newsletter with no articles."""
    newsletter = Newsletter("Empty News")
    assert newsletter.get_latest_article() == ""
    assert newsletter.get_article_count() == 0


def test_weather_station_get_pressure():
    """Test that the station reports the pressure it was given."""
    station = WeatherStation()
    station.set_measurements(25.0, 60.0, 1013.25)

    assert station.get_pressure() == 1013.25
