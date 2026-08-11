"""Tests for the Factory pattern."""

import pytest

from design_patterns.creational.factory import AnimalFactory


def test_factory_creates_dog():
    """Test that factory creates a Dog instance correctly."""
    factory = AnimalFactory()
    dog = factory.get_animal("dog", "Buddy")
    assert dog.name == "Buddy"
    assert dog.speak() == "Buddy says woof!"


def test_factory_creates_cat():
    """Test that factory creates a Cat instance correctly."""
    factory = AnimalFactory()
    cat = factory.get_animal("cat", "Whiskers")
    assert cat.name == "Whiskers"
    assert cat.speak() == "Whiskers says meow!"


def test_factory_raises_error_for_invalid_type():
    """Test that factory raises ValueError for invalid animal type."""
    factory = AnimalFactory()
    with pytest.raises(ValueError, match="Unknown animal type: bird"):
        factory.get_animal("bird", "Tweety")


def test_factory_case_sensitive():
    """Test that factory is case-sensitive for animal types."""
    factory = AnimalFactory()
    with pytest.raises(ValueError, match="Unknown animal type: Dog"):
        factory.get_animal("Dog", "Buddy")
