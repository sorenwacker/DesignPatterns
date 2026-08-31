"""Composition Pattern Example

This module demonstrates the Composition design pattern in Python
with a `Car` class composed of `Engine` and `Wheel` classes.
The `Car` class encapsulates the functionality of its components,
showcasing how objects can be composed to build more complex
structures.
"""


class Engine:
    """Represents a car engine."""

    def start(self) -> str:
        """Starts the engine.

        Returns:
            str: A message indicating the engine has started.
        """
        return "Engine started."


class Wheel:
    """Represents a wheel of the car."""

    def rotate(self) -> str:
        """Rotates the wheel.

        Returns:
            str: A message indicating the wheel is rotating.
        """
        return "Wheel is rotating."


class Car:
    """Represents a car composed of an engine and wheels."""

    def __init__(self) -> None:
        """Initializes a Car instance with an engine and four wheels."""
        self.engine = Engine()  # Composition, Car has an engine
        self.wheels = [Wheel() for _ in range(4)]  # Car has 4 wheels

    def drive(self) -> str:
        """Drives the car, starting the engine and rotating the wheels.

        Returns:
            str: A message indicating the car is driving.
        """
        return (
            self.engine.start()
            + " "
            + " ".join(wheel.rotate() for wheel in self.wheels)
        )
