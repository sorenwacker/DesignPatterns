"""Tests for the Composite pattern."""

from design_patterns.structural.composite import (
    Circle,
    CompositeShape,
    Rectangle,
    Shape,
)


def test_circle_draw():
    """Test that Circle draws correctly."""
    circle = Circle()
    assert circle.draw() == "Drawing a circle."


def test_rectangle_draw():
    """Test that Rectangle draws correctly."""
    rectangle = Rectangle()
    assert rectangle.draw() == "Drawing a rectangle."


def test_composite_shape_empty():
    """Test that empty CompositeShape returns correct string."""
    composite = CompositeShape()
    assert composite.draw() == "Composite Shape: "


def test_composite_shape_single_element():
    """Test CompositeShape with a single shape."""
    composite = CompositeShape()
    composite.add(Circle())
    assert composite.draw() == "Composite Shape: Drawing a circle."


def test_composite_shape_multiple_elements():
    """Test CompositeShape with multiple shapes."""
    composite = CompositeShape()
    composite.add(Circle())
    composite.add(Rectangle())
    assert (
        composite.draw() == "Composite Shape: Drawing a circle., Drawing a rectangle."
    )


def test_composite_shape_nested():
    """Test nested CompositeShape."""
    inner_composite = CompositeShape()
    inner_composite.add(Circle())
    inner_composite.add(Rectangle())

    outer_composite = CompositeShape()
    outer_composite.add(Circle())
    outer_composite.add(inner_composite)

    result = outer_composite.draw()
    assert "Drawing a circle." in result
    assert "Composite Shape:" in result


def test_composite_shape_is_shape():
    """Test that CompositeShape is a Shape."""
    composite = CompositeShape()
    assert isinstance(composite, Shape)
