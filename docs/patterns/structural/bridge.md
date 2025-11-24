# Bridge Pattern

**Category:** Structural Pattern

## Overview

Decouple an abstraction from its implementation so that the two can vary independently. This pattern uses composition over inheritance to separate the interface from the implementation, allowing both to be extended independently without affecting each other.

## Usage Guidelines

**Use when:**
- Want to avoid permanent binding between abstraction and implementation
- Both abstraction and implementation should be extended independently
- Need to switch implementations at runtime
- Multiple implementations of abstraction exist

**Avoid when:**
- Only one implementation exists
- Implementation doesn't vary
- Simple inheritance suffices
- Extra indirection is unacceptable for performance

## Implementation

```python
from __future__ import annotations
from abc import ABC, abstractmethod

# Implementation Interface
class Renderer(ABC):
    """Abstract implementation interface for rendering."""

    @abstractmethod
    def render_circle(self, radius: float) -> str:
        """Render a circle."""
        pass

    @abstractmethod
    def render_square(self, side: float) -> str:
        """Render a square."""
        pass

# Concrete Implementations
class VectorRenderer(Renderer):
    """Concrete implementation for vector rendering."""

    def render_circle(self, radius: float) -> str:
        """Render circle as vector."""
        return f"Drawing circle with radius {radius} as vector"

    def render_square(self, side: float) -> str:
        """Render square as vector."""
        return f"Drawing square with side {side} as vector"

class RasterRenderer(Renderer):
    """Concrete implementation for raster rendering."""

    def render_circle(self, radius: float) -> str:
        """Render circle as raster."""
        return f"Drawing circle with radius {radius} as pixels"

    def render_square(self, side: float) -> str:
        """Render square as raster."""
        return f"Drawing square with side {side} as pixels"

# Abstraction
class Shape(ABC):
    """Abstract shape class using bridge to renderer."""

    def __init__(self, renderer: Renderer) -> None:
        """Initialize shape with a renderer."""
        self.renderer = renderer

    @abstractmethod
    def draw(self) -> str:
        """Draw the shape."""
        pass

    @abstractmethod
    def resize(self, factor: float) -> None:
        """Resize the shape."""
        pass

# Refined Abstractions
class Circle(Shape):
    """Concrete circle shape."""

    def __init__(self, renderer: Renderer, radius: float = 5.0) -> None:
        """Initialize circle."""
        super().__init__(renderer)
        self.radius = radius

    def draw(self) -> str:
        """Draw circle using renderer."""
        return self.renderer.render_circle(self.radius)

    def resize(self, factor: float) -> None:
        """Resize circle."""
        self.radius *= factor

class Square(Shape):
    """Concrete square shape."""

    def __init__(self, renderer: Renderer, side: float = 5.0) -> None:
        """Initialize square."""
        super().__init__(renderer)
        self.side = side

    def draw(self) -> str:
        """Draw square using renderer."""
        return self.renderer.render_square(self.side)

    def resize(self, factor: float) -> None:
        """Resize square."""
        self.side *= factor
```

### Usage

```python
# Create shapes with different renderers
circle_vector = Circle(VectorRenderer(), 5.0)
print(circle_vector.draw())  # Drawing circle with radius 5.0 as vector

circle_raster = Circle(RasterRenderer(), 5.0)
print(circle_raster.draw())  # Drawing circle with radius 5.0 as pixels

square_vector = Square(VectorRenderer(), 10.0)
print(square_vector.draw())  # Drawing square with side 10.0 as vector

# Resize and redraw
circle_vector.resize(2.0)
print(circle_vector.draw())  # Drawing circle with radius 10.0 as vector
```

## Trade-offs

**Benefits:**
1. Abstraction and implementation can vary independently
2. Implementation can be selected or switched at runtime
3. Isolates platform-specific code
4. New abstractions and implementations without changing existing code (Open/Closed Principle)

**Drawbacks:**
1. Adds complexity with additional abstractions
2. Extra layer of indirection
3. Can be hard to design proper abstraction/implementation split
4. Too complex for simple scenarios

## Real-World Examples

- GUI frameworks separating GUI from platform-specific rendering
- Database drivers with abstract operations from specific implementations
- Graphics systems separating shapes from rendering methods
- Device drivers separating operations from hardware implementations

## Related Patterns

- Abstract Factory
- Adapter
- State

## API Reference

::: design_patterns.structural.bridge
    options:
      show_root_heading: true
      show_source: true
