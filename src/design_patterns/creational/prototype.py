"""Prototype Pattern Module

The Prototype pattern creates new objects by cloning existing instances rather than
creating new ones from scratch. This is useful when object creation is expensive or
when you want to avoid the complexity of instantiating an object directly.

Python provides built-in support for prototyping through the `copy` module, which
offers both shallow and deep copying mechanisms.

Example:
    Cloning a document with its formatting:

    ```python
    original = Document("Report", "Arial", 12)
    original.add_section("Introduction")

    # Shallow copy - shared references
    copy1 = original.clone()

    # Deep copy - independent copy
    copy2 = original.deep_clone()
    ```
"""

from __future__ import annotations

import copy
from typing import Any


class Prototype:
    """Abstract base class for prototypes.

    Defines the interface for cloning objects.
    """

    def clone(self) -> Prototype:
        """Create a shallow copy of the object.

        Returns:
            A shallow copy of the prototype.
        """
        return copy.copy(self)

    def deep_clone(self) -> Prototype:
        """Create a deep copy of the object.

        Returns:
            A deep copy of the prototype.
        """
        return copy.deepcopy(self)


class Document(Prototype):
    """Represents a document that can be cloned.

    This demonstrates the prototype pattern with both shallow and deep copying.
    """

    def __init__(self, title: str, font: str, font_size: int) -> None:
        """Initialize a document.

        Args:
            title: The document title.
            font: The font name.
            font_size: The font size.
        """
        self.title = title
        self.font = font
        self.font_size = font_size
        self.sections: list[str] = []
        self.metadata: dict[str, Any] = {}

    def add_section(self, section: str) -> None:
        """Add a section to the document.

        Args:
            section: The section name or content.
        """
        self.sections.append(section)

    def set_metadata(self, key: str, value: Any) -> None:
        """Set document metadata.

        Args:
            key: The metadata key.
            value: The metadata value.
        """
        self.metadata[key] = value

    def get_info(self) -> str:
        """Get document information.

        Returns:
            A string describing the document.
        """
        return (
            f"Document: {self.title}, "
            f"Font: {self.font} {self.font_size}pt, "
            f"Sections: {len(self.sections)}"
        )


class Shape(Prototype):
    """Represents a geometric shape that can be cloned.

    This demonstrates cloning with position and style attributes.
    """

    def __init__(self, x: int, y: int, color: str) -> None:
        """Initialize a shape.

        Args:
            x: X coordinate.
            y: Y coordinate.
            color: Shape color.
        """
        self.x = x
        self.y = y
        self.color = color

    def move(self, dx: int, dy: int) -> None:
        """Move the shape by the given deltas.

        Args:
            dx: Change in x coordinate.
            dy: Change in y coordinate.
        """
        self.x += dx
        self.y += dy

    def __repr__(self) -> str:
        """Return string representation of the shape.

        Returns:
            String representation.
        """
        return (
            f"{self.__class__.__name__}(x={self.x}, y={self.y}, color='{self.color}')"
        )


class Circle(Shape):
    """Represents a circle shape."""

    def __init__(self, x: int, y: int, color: str, radius: int) -> None:
        """Initialize a circle.

        Args:
            x: X coordinate of center.
            y: Y coordinate of center.
            color: Circle color.
            radius: Circle radius.
        """
        super().__init__(x, y, color)
        self.radius = radius

    def __repr__(self) -> str:
        """Return string representation of the circle.

        Returns:
            String representation.
        """
        return (
            f"Circle(x={self.x}, y={self.y}, "
            f"color='{self.color}', radius={self.radius})"
        )


class Rectangle(Shape):
    """Represents a rectangle shape."""

    def __init__(self, x: int, y: int, color: str, width: int, height: int) -> None:
        """Initialize a rectangle.

        Args:
            x: X coordinate of top-left corner.
            y: Y coordinate of top-left corner.
            color: Rectangle color.
            width: Rectangle width.
            height: Rectangle height.
        """
        super().__init__(x, y, color)
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        """Return string representation of the rectangle.

        Returns:
            String representation.
        """
        return (
            f"Rectangle(x={self.x}, y={self.y}, color='{self.color}', "
            f"width={self.width}, height={self.height})"
        )


class PrototypeRegistry:
    """Registry for managing prototype instances.

    This allows storing and retrieving prototype objects by name,
    which can then be cloned to create new instances.
    """

    def __init__(self) -> None:
        """Initialize an empty registry."""
        self._prototypes: dict[str, Prototype] = {}

    def register(self, name: str, prototype: Prototype) -> None:
        """Register a prototype with a given name.

        Args:
            name: The name to register the prototype under.
            prototype: The prototype object to register.
        """
        self._prototypes[name] = prototype

    def unregister(self, name: str) -> None:
        """Unregister a prototype.

        Args:
            name: The name of the prototype to unregister.
        """
        if name in self._prototypes:
            del self._prototypes[name]

    def clone(self, name: str) -> Prototype:
        """Clone a registered prototype.

        Args:
            name: The name of the prototype to clone.

        Returns:
            A shallow copy of the registered prototype.

        Raises:
            KeyError: If the prototype name is not registered.
        """
        if name not in self._prototypes:
            msg = f"Prototype '{name}' not found in registry"
            raise KeyError(msg)
        return self._prototypes[name].clone()

    def deep_clone(self, name: str) -> Prototype:
        """Deep clone a registered prototype.

        Args:
            name: The name of the prototype to clone.

        Returns:
            A deep copy of the registered prototype.

        Raises:
            KeyError: If the prototype name is not registered.
        """
        if name not in self._prototypes:
            msg = f"Prototype '{name}' not found in registry"
            raise KeyError(msg)
        return self._prototypes[name].deep_clone()
