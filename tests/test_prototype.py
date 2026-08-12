"""Tests for the Prototype pattern."""

import pytest

from design_patterns.creational.prototype import (
    Circle,
    Document,
    PrototypeRegistry,
    Rectangle,
)


def test_document_clone():
    """Test shallow cloning of a document."""
    doc1 = Document("Original", "Arial", 12)
    doc1.add_section("Introduction")

    doc2 = doc1.clone()

    assert doc2.title == "Original"
    assert doc2.font == "Arial"
    assert doc2.font_size == 12
    assert doc1 is not doc2


def test_document_shallow_copy_shares_list():
    """Test that shallow copy shares mutable objects."""
    doc1 = Document("Original", "Arial", 12)
    doc1.add_section("Introduction")

    doc2 = doc1.clone()
    doc2.add_section("Chapter 1")

    assert len(doc1.sections) == 2
    assert len(doc2.sections) == 2
    assert doc1.sections is doc2.sections


def test_document_deep_clone():
    """Test deep cloning of a document."""
    doc1 = Document("Original", "Arial", 12)
    doc1.add_section("Introduction")

    doc2 = doc1.deep_clone()
    doc2.add_section("Chapter 1")

    assert len(doc1.sections) == 1
    assert len(doc2.sections) == 2
    assert doc1.sections is not doc2.sections


def test_document_metadata_deep_clone():
    """Test that deep clone doesn't share metadata."""
    doc1 = Document("Original", "Arial", 12)
    doc1.set_metadata("author", "John Doe")

    doc2 = doc1.deep_clone()
    doc2.set_metadata("author", "Jane Smith")

    assert doc1.metadata["author"] == "John Doe"
    assert doc2.metadata["author"] == "Jane Smith"


def test_circle_clone():
    """Test cloning a circle."""
    circle1 = Circle(10, 20, "red", 5)
    circle2 = circle1.clone()

    assert circle2.x == 10
    assert circle2.y == 20
    assert circle2.color == "red"
    assert circle2.radius == 5
    assert circle1 is not circle2


def test_circle_clone_independence():
    """Test that cloned circle can be modified independently."""
    circle1 = Circle(10, 20, "red", 5)
    circle2 = circle1.clone()

    circle2.move(5, 10)
    circle2.color = "blue"

    assert circle1.x == 10
    assert circle1.y == 20
    assert circle1.color == "red"
    assert circle2.x == 15
    assert circle2.y == 30
    assert circle2.color == "blue"


def test_rectangle_clone():
    """Test cloning a rectangle."""
    rect1 = Rectangle(0, 0, "green", 100, 50)
    rect2 = rect1.clone()

    assert rect2.x == 0
    assert rect2.y == 0
    assert rect2.color == "green"
    assert rect2.width == 100
    assert rect2.height == 50
    assert rect1 is not rect2


def test_prototype_registry_register():
    """Test registering prototypes in the registry."""
    registry = PrototypeRegistry()
    circle = Circle(0, 0, "red", 10)

    registry.register("default_circle", circle)

    cloned = registry.clone("default_circle")
    assert isinstance(cloned, Circle)
    assert cloned.radius == 10


def test_prototype_registry_clone():
    """Test cloning from registry."""
    registry = PrototypeRegistry()
    doc = Document("Template", "Times", 14)
    doc.add_section("Header")

    registry.register("doc_template", doc)

    doc1 = registry.clone("doc_template")
    doc2 = registry.clone("doc_template")

    assert doc1 is not doc2
    assert doc1 is not doc
    assert isinstance(doc1, Document)


def test_prototype_registry_deep_clone():
    """Test deep cloning from registry."""
    registry = PrototypeRegistry()
    doc = Document("Template", "Times", 14)
    doc.add_section("Header")

    registry.register("doc_template", doc)

    doc1 = registry.deep_clone("doc_template")
    doc1.add_section("Body")

    doc2 = registry.deep_clone("doc_template")

    assert len(doc1.sections) == 2
    assert len(doc2.sections) == 1


def test_prototype_registry_unregister():
    """Test unregistering a prototype."""
    registry = PrototypeRegistry()
    circle = Circle(0, 0, "red", 10)

    registry.register("test_circle", circle)
    registry.unregister("test_circle")

    with pytest.raises(KeyError, match="Prototype 'test_circle' not found"):
        registry.clone("test_circle")


def test_prototype_registry_not_found():
    """Test cloning non-existent prototype."""
    registry = PrototypeRegistry()

    with pytest.raises(KeyError, match="Prototype 'nonexistent' not found"):
        registry.clone("nonexistent")


def test_shape_repr():
    """Test string representation of shapes."""
    circle = Circle(10, 20, "blue", 5)
    rect = Rectangle(5, 10, "green", 100, 50)

    assert "Circle" in repr(circle)
    assert "x=10" in repr(circle)
    assert "radius=5" in repr(circle)

    assert "Rectangle" in repr(rect)
    assert "width=100" in repr(rect)
    assert "height=50" in repr(rect)


def test_document_get_info():
    """Test that a document describes its own title, font, and size."""
    document = Document("Report", "Arial", 12)

    info = document.get_info()

    assert "Report" in info
    assert "Arial" in info
    assert "12" in info
