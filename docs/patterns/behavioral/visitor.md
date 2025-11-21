# Visitor Pattern

**Category:** Behavioral Pattern

## Intent

Represent an operation to be performed on elements of an object structure. The Visitor pattern lets you define new operations without changing the classes of the elements on which it operates. This pattern separates algorithms from the objects they operate on.

## Problem

When you need to perform operations on object structures, adding methods to classes leads to:

- Violating open/closed principle when adding new operations
- Scattering related operations across many classes
- Difficulty maintaining cohesive operations
- Mixing unrelated concerns in element classes
- Hard to add new operations without modifying existing classes

## When to Use

Use the Visitor pattern when:

- **Many operations**: Need to perform many distinct operations on object structure
- **Frequent new operations**: Operations change more frequently than object structure
- **Related operations**: Want to keep related operations together
- **Structure rarely changes**: Object structure is stable
- **Different element types**: Need to perform operations on different element types
- **Avoid class pollution**: Don't want to clutter classes with many operations

## When NOT to Use

Avoid the Visitor pattern when:

- **Frequent structure changes**: Object structure changes frequently
- **Few operations**: Only a few operations exist
- **Simple operations**: Operations are simple and well-suited as methods
- **Unstable interfaces**: Element interfaces change often
- **Complexity**: Pattern adds unnecessary complexity

## Structure

The Visitor pattern involves:

- **Visitor**: Interface declaring visit methods for each element type
- **Concrete Visitor**: Implements operations for each element type
- **Element**: Interface declaring accept method taking visitor
- **Concrete Elements**: Implement accept method calling appropriate visitor method
- **Object Structure**: Collection of elements that can be visited

## Implementation

### Shape Visitor Example

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

    @abstractmethod
    def visit_triangle(self, triangle: Triangle) -> str:
        """Visit a triangle."""
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

class Triangle(Shape):
    """Concrete triangle shape."""

    def __init__(self, base: float, height: float) -> None:
        """Initialize triangle."""
        self.base = base
        self.height = height

    def accept(self, visitor: ShapeVisitor) -> str:
        """Accept visitor for triangle."""
        return visitor.visit_triangle(self)

class AreaCalculator(ShapeVisitor):
    """Visitor that calculates areas of shapes."""

    def visit_circle(self, circle: Circle) -> str:
        """Calculate circle area."""
        import math
        area = math.pi * circle.radius ** 2
        return f"Circle area: {area:.2f}"

    def visit_rectangle(self, rectangle: Rectangle) -> str:
        """Calculate rectangle area."""
        area = rectangle.width * rectangle.height
        return f"Rectangle area: {area:.2f}"

    def visit_triangle(self, triangle: Triangle) -> str:
        """Calculate triangle area."""
        area = (triangle.base * triangle.height) / 2
        return f"Triangle area: {area:.2f}"

class PerimeterCalculator(ShapeVisitor):
    """Visitor that calculates perimeters of shapes."""

    def visit_circle(self, circle: Circle) -> str:
        """Calculate circle perimeter."""
        import math
        perimeter = 2 * math.pi * circle.radius
        return f"Circle perimeter: {perimeter:.2f}"

    def visit_rectangle(self, rectangle: Rectangle) -> str:
        """Calculate rectangle perimeter."""
        perimeter = 2 * (rectangle.width + rectangle.height)
        return f"Rectangle perimeter: {perimeter:.2f}"

    def visit_triangle(self, triangle: Triangle) -> str:
        """Calculate triangle perimeter (assumes right triangle)."""
        import math
        hypotenuse = math.sqrt(triangle.base**2 + triangle.height**2)
        perimeter = triangle.base + triangle.height + hypotenuse
        return f"Triangle perimeter: {perimeter:.2f}"

class XMLExporter(ShapeVisitor):
    """Visitor that exports shapes to XML format."""

    def visit_circle(self, circle: Circle) -> str:
        """Export circle to XML."""
        return f'<Circle radius="{circle.radius}"/>'

    def visit_rectangle(self, rectangle: Rectangle) -> str:
        """Export rectangle to XML."""
        return f'<Rectangle width="{rectangle.width}" height="{rectangle.height}"/>'

    def visit_triangle(self, triangle: Triangle) -> str:
        """Export triangle to XML."""
        return f'<Triangle base="{triangle.base}" height="{triangle.height}"/>'

class JSONExporter(ShapeVisitor):
    """Visitor that exports shapes to JSON format."""

    def visit_circle(self, circle: Circle) -> str:
        """Export circle to JSON."""
        return f'{{"type": "circle", "radius": {circle.radius}}}'

    def visit_rectangle(self, rectangle: Rectangle) -> str:
        """Export rectangle to JSON."""
        return f'{{"type": "rectangle", "width": {rectangle.width}, "height": {rectangle.height}}}'

    def visit_triangle(self, triangle: Triangle) -> str:
        """Export triangle to JSON."""
        return f'{{"type": "triangle", "base": {triangle.base}, "height": {triangle.height}}}'

class ShapeCollection:
    """Collection of shapes that can be visited."""

    def __init__(self) -> None:
        """Initialize empty shape collection."""
        self.shapes: list[Shape] = []

    def add_shape(self, shape: Shape) -> None:
        """Add a shape to the collection."""
        self.shapes.append(shape)

    def accept_all(self, visitor: ShapeVisitor) -> list[str]:
        """Apply visitor to all shapes."""
        return [shape.accept(visitor) for shape in self.shapes]
```

## Usage Example

```python
# Create shapes
circle = Circle(5.0)
rectangle = Rectangle(4.0, 6.0)
triangle = Triangle(3.0, 4.0)

# Calculate areas
area_calc = AreaCalculator()
print(circle.accept(area_calc))  # Circle area: 78.54
print(rectangle.accept(area_calc))  # Rectangle area: 24.00
print(triangle.accept(area_calc))  # Triangle area: 6.00

# Calculate perimeters
perimeter_calc = PerimeterCalculator()
print(circle.accept(perimeter_calc))  # Circle perimeter: 31.42
print(rectangle.accept(perimeter_calc))  # Rectangle perimeter: 20.00
print(triangle.accept(perimeter_calc))  # Triangle perimeter: 12.00

# Export to XML
xml_exporter = XMLExporter()
print(circle.accept(xml_exporter))  # <Circle radius="5.0"/>
print(rectangle.accept(xml_exporter))  # <Rectangle width="4.0" height="6.0"/>

# Export to JSON
json_exporter = JSONExporter()
print(circle.accept(json_exporter))  # {"type": "circle", "radius": 5.0}

# Use with collection
collection = ShapeCollection()
collection.add_shape(circle)
collection.add_shape(rectangle)
collection.add_shape(triangle)

# Apply visitor to all shapes
areas = collection.accept_all(area_calc)
print(areas)  # List of all area calculations
```

## Key Benefits

1. **Open/Closed Principle**: Add new operations without modifying elements
2. **Single Responsibility**: Groups related operations in visitor classes
3. **Accumulate state**: Visitor can accumulate state while traversing
4. **Separate concerns**: Separates algorithms from object structure
5. **Easy to add operations**: New visitors add new operations easily
6. **Type safety**: Compiler ensures all element types are handled

## Drawbacks

1. **Breaking encapsulation**: Visitor may need access to element internals
2. **Adding elements difficult**: Adding new element types requires updating all visitors
3. **Circular dependencies**: Element and visitor interfaces reference each other
4. **Complexity**: Adds conceptual and implementation complexity
5. **Not intuitive**: Double dispatch mechanism can be confusing

## Real-World Examples

- **Compiler AST**: Operations on abstract syntax trees (type checking, code generation)
- **Document processing**: Rendering, exporting, validating documents
- **File system operations**: Computing sizes, searching, archiving
- **Graphics rendering**: Different rendering for different shapes
- **Report generation**: Generating reports in various formats
- **Tax calculation**: Calculating taxes for different income sources
- **Game entity operations**: Rendering, collision detection, AI behavior

## Related Patterns

- **Composite**: Visitor often operates on composite structures
- **Iterator**: Visitor can use iterator to traverse structure
- **Interpreter**: Visitor can interpret expressions in syntax trees
- **Strategy**: Similar structure but visitor operates on heterogeneous objects

## API Reference

::: design_patterns.behavioral.visitor
    options:
      show_root_heading: true
      show_source: true
