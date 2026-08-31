"""Tests for the Inheritance principle example."""

import pytest

from design_patterns.structural.inheritance import Animal, Cat, Dog


def test_dog_speak():
    """Test that Dog speaks correctly."""
    dog = Dog("Buddy")
    assert dog.speak() == "Buddy says woof!"


def test_cat_speak():
    """Test that Cat speaks correctly."""
    cat = Cat("Whiskers")
    assert cat.speak() == "Whiskers says meow!"


def test_dog_name():
    """Test that Dog has correct name."""
    dog = Dog("Max")
    assert dog.name == "Max"


def test_cat_name():
    """Test that Cat has correct name."""
    cat = Cat("Fluffy")
    assert cat.name == "Fluffy"


def test_dog_is_animal():
    """Test that Dog is an Animal."""
    dog = Dog("Buddy")
    assert isinstance(dog, Animal)


def test_cat_is_animal():
    """Test that Cat is an Animal."""
    cat = Cat("Whiskers")
    assert isinstance(cat, Animal)


def test_animal_cannot_be_instantiated():
    """Animal is abstract; only concrete animals can be created."""
    with pytest.raises(TypeError, match="abstract"):
        Animal("Generic")  # type: ignore[abstract]
