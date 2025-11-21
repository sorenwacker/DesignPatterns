# Prototype Pattern

**Category:** Creational Pattern

## Intent

Create new objects by cloning existing instances rather than creating new ones from scratch. The Prototype pattern is useful when object creation is expensive or when you want to avoid the complexity of instantiating an object directly. Python provides built-in support through the `copy` module.

## Problem

Creating objects from scratch can be problematic when:

- Object initialization is expensive (complex calculations, database queries, file I/O)
- Objects have many configurations that are tedious to set up
- You want to create copies while hiding the complexity of copying
- The exact types to create aren't known until runtime
- Classes to instantiate are specified at runtime
- Creating objects requires coupling to specific concrete classes

## When to Use

Use the Prototype pattern when:

- **Expensive creation**: Creating new objects is more expensive than cloning existing ones
- **Complex initialization**: Objects require complex setup that can be reused
- **Runtime specification**: Types to create are determined at runtime
- **Avoid subclassing**: Want to avoid creating factory hierarchies for each product variant
- **State preservation**: Need copies of objects in specific states
- **Registry of prototypes**: Maintaining a catalog of prototype objects to clone
- **Independent copies**: Need objects that can be modified independently

## When NOT to Use

Avoid the Prototype pattern when:

- **Simple objects**: Creating new objects is straightforward and cheap
- **Deep vs shallow copy confusion**: Complexity of managing object references outweighs benefits
- **Unique objects**: Each object must be unique with distinct identity
- **Circular references**: Objects contain circular references that complicate cloning
- **Immutable objects**: Objects are immutable and can be safely shared
- **No initialization cost**: Object creation cost is negligible

## Structure

The Prototype pattern involves:

- **Prototype Interface**: Declares cloning methods (clone, deep_clone)
- **Concrete Prototypes**: Implement cloning operations
- **Client**: Creates new objects by cloning prototypes
- **Prototype Registry** (optional): Maintains a catalog of available prototypes
- **Shallow Copy**: Copies object but shares references to nested objects
- **Deep Copy**: Recursively copies object and all nested objects

## Implementation

### Basic Prototype with Document Example

```python
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
        return (f"Document: {self.title}, "
                f"Font: {self.font} {self.font_size}pt, "
                f"Sections: {len(self.sections)}")
```

### Shape Hierarchy Example

```python
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
        """Return string representation of the shape."""
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, color='{self.color}')"

class Circle(Shape):
    """Represents a circle shape."""

    def __init__(self, x: int, y: int, color: str, radius: int) -> None:
        """Initialize a circle."""
        super().__init__(x, y, color)
        self.radius = radius

    def __repr__(self) -> str:
        """Return string representation of the circle."""
        return f"Circle(x={self.x}, y={self.y}, color='{self.color}', radius={self.radius})"

class Rectangle(Shape):
    """Represents a rectangle shape."""

    def __init__(self, x: int, y: int, color: str, width: int, height: int) -> None:
        """Initialize a rectangle."""
        super().__init__(x, y, color)
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        """Return string representation of the rectangle."""
        return (f"Rectangle(x={self.x}, y={self.y}, color='{self.color}', "
                f"width={self.width}, height={self.height})")
```

### Prototype Registry

```python
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
            raise KeyError(f"Prototype '{name}' not found in registry")
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
            raise KeyError(f"Prototype '{name}' not found in registry")
        return self._prototypes[name].deep_clone()
```

## Usage Example

```python
# Create original document
original = Document("Report", "Arial", 12)
original.add_section("Introduction")
original.add_section("Methodology")
original.set_metadata("author", "John Doe")

# Shallow copy - shares mutable references
shallow_copy = original.clone()
shallow_copy.title = "Modified Report"
shallow_copy.add_section("Results")  # Affects original too!

# Deep copy - independent copy
deep_copy = original.deep_clone()
deep_copy.title = "Independent Report"
deep_copy.add_section("Conclusion")  # Does NOT affect original

print(f"Original sections: {len(original.sections)}")  # 3
print(f"Deep copy sections: {len(deep_copy.sections)}")  # 4

# Using shapes with registry
registry = PrototypeRegistry()

# Register prototypes
red_circle = Circle(0, 0, "red", 10)
blue_rect = Rectangle(0, 0, "blue", 20, 30)

registry.register("circle", red_circle)
registry.register("rectangle", blue_rect)

# Clone from registry
circle_copy = registry.clone("circle")
circle_copy.move(5, 5)
circle_copy.color = "green"

print(red_circle)  # Circle(x=0, y=0, color='red', radius=10)
print(circle_copy)  # Circle(x=5, y=5, color='green', radius=10)
```

## Key Benefits

1. **Performance**: Cloning can be faster than creating objects from scratch
2. **Flexibility**: Add or remove prototypes at runtime
3. **Reduced subclassing**: Avoid factory hierarchies for product variants
4. **State preservation**: Clone objects in specific configured states
5. **Hides complexity**: Cloning encapsulates complex copying logic
6. **Runtime configuration**: Specify products at runtime by cloning prototypes
7. **Independent copies**: Each clone can be modified independently (with deep copy)

## Drawbacks

1. **Shallow vs deep copy**: Managing copy semantics can be tricky
2. **Circular references**: Objects with circular references are hard to clone
3. **Clone method complexity**: Implementing proper cloning can be complex
4. **Hidden dependencies**: Cloning may not work correctly with certain object graphs
5. **Prototype management**: Registry adds overhead and complexity
6. **Initialization**: Cloned objects may need additional initialization

## Real-World Examples

- **Document templates**: Cloning pre-configured document templates
- **Game objects**: Cloning enemy types, weapons, or items with preset configurations
- **Graphics editors**: Cloning shapes, images, or design elements
- **Configuration objects**: Cloning configuration presets
- **Database records**: Cloning row templates with default values
- **Test fixtures**: Cloning test data objects for different test cases
- **UI components**: Cloning pre-configured UI widgets
- **Network packets**: Cloning packet templates with standard headers

## Related Patterns

- **Abstract Factory**: Prototype can be simpler alternative to Abstract Factory
- **Composite**: Often combined with Prototype to clone composite trees
- **Decorator**: Prototypes with decorators can clone decorated objects
- **Memento**: Can use Prototype to implement memento snapshots
- **Singleton**: Singleton prevents cloning, opposite of Prototype

## API Reference

::: design_patterns.creational.prototype
    options:
      show_root_heading: true
      show_source: true
