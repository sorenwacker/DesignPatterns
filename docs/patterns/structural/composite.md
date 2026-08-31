# Composite Pattern

**Category:** Structural Pattern

## Overview

Compose objects into tree structures to represent part-whole hierarchies. This pattern lets clients treat individual objects and compositions of objects uniformly, enabling building of complex structures from simple components.

## Usage Guidelines

**Use when:**

- Need to represent part-whole hierarchies
- Want to treat individual and composite objects uniformly
- Objects can contain other objects of same type
- Working with hierarchical data structures

**Avoid when:**

- Structure is flat, not hierarchical
- Leaves and composites require very different operations
- Need strong type distinctions between components
- Tree traversal overhead is unacceptable for performance

## Implementation

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    """Base class for all shapes."""

    @abstractmethod
    def draw(self) -> str:
        """Draws the shape.

        Returns:
            str: A description of what was drawn.
        """

class Circle(Shape):
    """Represents a circle shape."""

    def draw(self) -> str:
        return "Drawing a circle."

class Rectangle(Shape):
    """Represents a rectangle shape."""

    def draw(self) -> str:
        return "Drawing a rectangle."

class CompositeShape(Shape):
    """A composite shape that can contain other shapes."""

    def __init__(self):
        """Initializes a CompositeShape with an empty list of shapes."""
        self.shapes = []

    def add(self, shape: Shape) -> None:
        """Adds a shape to the composite shape.

        Args:
            shape: The shape to be added.
        """
        self.shapes.append(shape)

    def remove(self, shape: Shape) -> None:
        """Removes a shape from the composite shape.

        Args:
            shape: The shape to be removed.
        """
        if shape in self.shapes:
            self.shapes.remove(shape)

    def draw(self) -> str:
        """Draws all shapes in the composite shape.

        Returns:
            str: A string representation of all drawn shapes.
        """
        return "Composite Shape: " + ", ".join(shape.draw() for shape in self.shapes)
```

### Usage

```python
# Create individual shapes
circle = Circle()
rectangle = Rectangle()

# Create composite
composite = CompositeShape()
composite.add(circle)
composite.add(rectangle)

# Draw individual shape
print(circle.draw())  # Drawing a circle.

# Draw composite (draws all contained shapes)
print(composite.draw())  # Composite Shape: Drawing a circle., Drawing a rectangle.

# Create nested composite
main_composite = CompositeShape()
main_composite.add(Circle())
main_composite.add(composite)

# Draw nested structure
print(main_composite.draw())
# Composite Shape: Drawing a circle., Composite Shape: Drawing a circle., Drawing a rectangle.
```

## Trade-offs

**Benefits:**

1. Clients treat simple and complex objects uniformly
2. Easy to create complex tree structures through recursive composition
3. Easy to add new component types (Open/Closed Principle)
4. Simplified client code that doesn't distinguish between types

**Drawbacks:**

1. Makes design overly general
2. Hard to restrict component types for type safety
3. Leaf-specific operations complicate interface
4. Traversing deep trees can be slow

## Real-World Examples

- File systems with files and directories
- GUI components with windows, panels, buttons
- Graphics scenes with shapes, groups, scenes
- Menu systems with menu items and submenus

## Related Patterns

- Iterator
- Visitor
- Decorator
- Flyweight

## API Reference

::: design_patterns.structural.composite
    options:
      show_root_heading: true
      show_source: true
