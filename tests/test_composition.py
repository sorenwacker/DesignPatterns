"""Tests for the Composition principle example."""

from design_patterns.structural.composition import Car, Engine, Wheel


def test_engine_start():
    """Test that Engine starts correctly."""
    engine = Engine()
    assert engine.start() == "Engine started."


def test_wheel_rotate():
    """Test that Wheel rotates correctly."""
    wheel = Wheel()
    assert wheel.rotate() == "Wheel is rotating."


def test_car_has_engine():
    """Test that Car has an Engine."""
    car = Car()
    assert isinstance(car.engine, Engine)


def test_car_has_wheels():
    """Test that Car has four wheels."""
    car = Car()
    assert len(car.wheels) == 4
    assert all(isinstance(wheel, Wheel) for wheel in car.wheels)


def test_car_drive():
    """Test that Car drives correctly."""
    car = Car()
    result = car.drive()
    assert "Engine started." in result
    assert "Wheel is rotating." in result
    assert result.count("Wheel is rotating.") == 4
