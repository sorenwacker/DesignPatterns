# Visitor Pattern

**Category:** Behavioral Pattern

## Overview

Represent an operation to be performed on elements of an object structure. This pattern lets you define new operations without changing the classes of the elements on which it operates, separating algorithms from the objects they operate on.

## Usage Guidelines

**Use when:**

- Need to perform many distinct operations on object structure
- Operations change more frequently than object structure
- Want to keep related operations together
- Object structure is stable but operations vary

**Avoid when:**

- Object structure changes frequently
- Only a few operations exist
- Operations are simple and well-suited as methods
- Element interfaces change often

## Implementation

```python
from __future__ import annotations
from abc import ABC, abstractmethod

class ShapeVisitor(ABC):
    """Abstract visitor for shape operations."""

    @abstractmethod
    def visit_circle(self, circle: Circle) -> str:
        """Visit a circle."""
        pass

    @abstractmethod
    def visit_rectangle(self, rectangle: Rectangle) -> str:
        """Visit a rectangle."""
        pass

class Shape(ABC):
    """Abstract shape that accepts visitors."""

    @abstractmethod
    def accept(self, visitor: ShapeVisitor) -> str:
        """Accept a visitor."""
        pass

class Circle(Shape):
    """Concrete circle shape."""

    def __init__(self, radius: float) -> None:
        """Initialize circle."""
        self.radius = radius

    def accept(self, visitor: ShapeVisitor) -> str:
        """Accept visitor for circle."""
        return visitor.visit_circle(self)

class Rectangle(Shape):
    """Concrete rectangle shape."""

    def __init__(self, width: float, height: float) -> None:
        """Initialize rectangle."""
        self.width = width
        self.height = height

    def accept(self, visitor: ShapeVisitor) -> str:
        """Accept visitor for rectangle."""
        return visitor.visit_rectangle(self)

class AreaCalculator(ShapeVisitor):
    """Visitor that calculates areas of shapes."""

    def visit_circle(self, circle: Circle) -> str:
        """Calculate circle area."""
        area = math.pi * circle.radius ** 2
        return f"Circle area: {area:.2f}"

    def visit_rectangle(self, rectangle: Rectangle) -> str:
        """Calculate rectangle area."""
        area = rectangle.width * rectangle.height
        return f"Rectangle area: {area:.2f}"
```

### Usage

```python
# Create shapes
circle = Circle(5.0)
rectangle = Rectangle(4.0, 6.0)

# Calculate areas
area_calc = AreaCalculator()
print(circle.accept(area_calc))  # Circle area: 78.54
print(rectangle.accept(area_calc))  # Rectangle area: 24.00
```

## Trade-offs

**Benefits:**

1. Add new operations without modifying elements (Open/Closed Principle)
2. Groups related operations in visitor classes (Single Responsibility)
3. Visitor can accumulate state while traversing
4. Separates algorithms from object structure

**Drawbacks:**

1. Visitor may need access to element internals breaking encapsulation
2. Adding new element types requires updating all visitors
3. Circular dependencies between element and visitor interfaces
4. Double dispatch mechanism can be confusing

## Real-World Examples

- Compiler AST operations like type checking and code generation
- Document processing with rendering, exporting, validating
- File system operations computing sizes, searching, archiving
- Graphics rendering for different shapes

## Related Patterns

- Composite
- Iterator
- Interpreter
- Strategy

## API Reference

::: design_patterns.behavioral.visitor
    options:
      show_root_heading: true
      show_source: true
