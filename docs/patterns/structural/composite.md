# Composite Pattern

**Category:** Structural Pattern

## Intent

Compose objects into tree structures to represent part-whole hierarchies. The Composite pattern lets clients treat individual objects and compositions of objects uniformly, enabling building of complex structures from simple components.

## Problem

When working with tree structures, treating individual and composite objects differently leads to:

- Complex client code with type checking
- Difficulty adding new component types
- Inconsistent treatment of leaves and composites
- Hard to build recursive structures
- Violation of open/closed principle

## When to Use

Use the Composite pattern when:

- **Tree structures**: Need to represent part-whole hierarchies
- **Uniform treatment**: Want to treat individual and composite objects uniformly
- **Recursive composition**: Objects can contain other objects of same type
- **Hierarchical data**: Working with hierarchical data structures
- **Graphics scenes**: Building graphics scenes with nested elements
- **File systems**: Representing files and directories

## When NOT to Use

Avoid the Composite pattern when:

- **No hierarchy**: Structure is flat, not hierarchical
- **Different operations**: Leaves and composites require very different operations
- **Type safety**: Need strong type distinctions between components
- **Simple structure**: Structure doesn't justify pattern complexity
- **Performance critical**: Tree traversal overhead is unacceptable

## Structure

The Composite pattern involves:

- **Component**: Interface for all objects in composition
- **Leaf**: Represents leaf objects with no children
- **Composite**: Defines behavior for components with children
- **Client**: Manipulates objects through component interface

## Implementation

### Graphics Example

```python
class Shape:
    """Base class for all shapes."""

    def draw(self) -> str:
        """Draws the shape.

        Raises:
            NotImplementedError: Subclasses must implement this method.
        """
        raise NotImplementedError("Subclasses must implement this method.")

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

## Usage Example

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

## Key Benefits

1. **Uniform treatment**: Clients treat simple and complex objects uniformly
2. **Recursive composition**: Easy to create complex tree structures
3. **Open/Closed Principle**: Easy to add new component types
4. **Simplified client code**: Client doesn't need to distinguish between types
5. **Flexibility**: Can build arbitrarily complex structures

## Drawbacks

1. **Overly general**: Makes design overly general
2. **Type safety**: Hard to restrict component types
3. **Leaf operations**: Leaf-specific operations complicate interface
4. **Design challenge**: Can be hard to design clean component interface
5. **Performance**: Traversing deep trees can be slow

## Real-World Examples

- **File systems**: Files and directories
- **GUI components**: Windows, panels, buttons
- **Organization charts**: Employees and departments
- **Graphics scenes**: Shapes, groups, scenes
- **Menu systems**: Menu items and submenus
- **XML/HTML DOM**: Elements and nested elements
- **Expression trees**: Operators and operands

## Related Patterns

- **Iterator**: Can use Iterator to traverse composite structures
- **Visitor**: Can apply operations to composite structures
- **Decorator**: Often used together with Composite
- **Flyweight**: Can share composite components to save memory

## API Reference

::: design_patterns.structural.composite
    options:
      show_root_heading: true
      show_source: true
