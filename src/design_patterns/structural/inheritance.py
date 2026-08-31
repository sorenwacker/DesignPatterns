"""Inheritance Pattern Example

This module demonstrates the inheritance design pattern in Python
using an `Animal` base class and its subclasses `Dog` and `Cat`.
The `Animal` class defines a common interface that requires
subclasses to implement the `speak` method, providing specific
implementations for different animal types.
"""

from abc import ABC, abstractmethod


class Animal(ABC):
    """Base class for all animals.

    This class defines the common interface for all animal types,
    requiring subclasses to implement the `speak` method.

    Attributes:
        name (str): The name of the animal.

    Usage:
        ```
        class Dog(Animal):
            def speak(self) -> str:
                return f"{self.name} says woof!"
        ```
    """

    def __init__(self, name: str) -> None:
        """Initializes an Animal instance.

        Args:
            name: The name of the animal.
        """
        self.name = name

    @abstractmethod
    def speak(self) -> str:
        """Produce the sound this animal makes.

        Returns:
            str: A sentence naming the animal and its sound.
        """


class Dog(Animal):
    """Class representing a dog, a type of Animal."""

    def speak(self) -> str:
        """Bark.

        Returns:
            str: The dog's name and its sound.
        """
        return f"{self.name} says woof!"


class Cat(Animal):
    """Class representing a cat, a type of Animal."""

    def speak(self) -> str:
        """Meow.

        Returns:
            str: The cat's name and its sound.
        """
        return f"{self.name} says meow!"
