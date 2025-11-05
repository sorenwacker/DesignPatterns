"""Visitor Pattern Module

The Visitor pattern represents an operation to be performed on elements of an object
structure. It lets you define new operations without changing the classes of the
elements on which it operates. This pattern separates algorithms from the objects
they operate on.

Example:
    Calculating areas and exporting shapes:

    ```python
    circle = Circle(5)
    rectangle = Rectangle(4, 6)

    area_calculator = AreaCalculator()
    print(circle.accept(area_calculator))  # Area: 78.54
    print(rectangle.accept(area_calculator))  # Area: 24

    exporter = XMLExporter()
    print(circle.accept(exporter))  # <Circle radius="5"/>
    ```
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class ShapeVisitor(ABC):
    """Abstract visitor for shape operations."""

    @abstractmethod
    def visit_circle(self, circle: Circle) -> str:
        """Visit a circle.

        Args:
            circle: Circle to visit.

        Returns:
            Result of visiting the circle.
        """
        pass

    @abstractmethod
    def visit_rectangle(self, rectangle: Rectangle) -> str:
        """Visit a rectangle.

        Args:
            rectangle: Rectangle to visit.

        Returns:
            Result of visiting the rectangle.
        """
        pass

    @abstractmethod
    def visit_triangle(self, triangle: Triangle) -> str:
        """Visit a triangle.

        Args:
            triangle: Triangle to visit.

        Returns:
            Result of visiting the triangle.
        """
        pass


class Shape(ABC):
    """Abstract shape that accepts visitors."""

    @abstractmethod
    def accept(self, visitor: ShapeVisitor) -> str:
        """Accept a visitor.

        Args:
            visitor: Visitor to accept.

        Returns:
            Result of the visit.
        """
        pass


class Circle(Shape):
    """Concrete circle shape."""

    def __init__(self, radius: float) -> None:
        """Initialize circle.

        Args:
            radius: Circle radius.
        """
        self.radius = radius

    def accept(self, visitor: ShapeVisitor) -> str:
        """Accept visitor for circle.

        Args:
            visitor: Visitor to accept.

        Returns:
            Result of visit.
        """
        return visitor.visit_circle(self)


class Rectangle(Shape):
    """Concrete rectangle shape."""

    def __init__(self, width: float, height: float) -> None:
        """Initialize rectangle.

        Args:
            width: Rectangle width.
            height: Rectangle height.
        """
        self.width = width
        self.height = height

    def accept(self, visitor: ShapeVisitor) -> str:
        """Accept visitor for rectangle.

        Args:
            visitor: Visitor to accept.

        Returns:
            Result of visit.
        """
        return visitor.visit_rectangle(self)


class Triangle(Shape):
    """Concrete triangle shape."""

    def __init__(self, base: float, height: float) -> None:
        """Initialize triangle.

        Args:
            base: Triangle base.
            height: Triangle height.
        """
        self.base = base
        self.height = height

    def accept(self, visitor: ShapeVisitor) -> str:
        """Accept visitor for triangle.

        Args:
            visitor: Visitor to accept.

        Returns:
            Result of visit.
        """
        return visitor.visit_triangle(self)


class AreaCalculator(ShapeVisitor):
    """Visitor that calculates areas of shapes."""

    def visit_circle(self, circle: Circle) -> str:
        """Calculate circle area.

        Args:
            circle: Circle to calculate.

        Returns:
            Area description.
        """
        import math
        area = math.pi * circle.radius ** 2
        return f"Circle area: {area:.2f}"

    def visit_rectangle(self, rectangle: Rectangle) -> str:
        """Calculate rectangle area.

        Args:
            rectangle: Rectangle to calculate.

        Returns:
            Area description.
        """
        area = rectangle.width * rectangle.height
        return f"Rectangle area: {area:.2f}"

    def visit_triangle(self, triangle: Triangle) -> str:
        """Calculate triangle area.

        Args:
            triangle: Triangle to calculate.

        Returns:
            Area description.
        """
        area = (triangle.base * triangle.height) / 2
        return f"Triangle area: {area:.2f}"


class PerimeterCalculator(ShapeVisitor):
    """Visitor that calculates perimeters of shapes."""

    def visit_circle(self, circle: Circle) -> str:
        """Calculate circle perimeter.

        Args:
            circle: Circle to calculate.

        Returns:
            Perimeter description.
        """
        import math
        perimeter = 2 * math.pi * circle.radius
        return f"Circle perimeter: {perimeter:.2f}"

    def visit_rectangle(self, rectangle: Rectangle) -> str:
        """Calculate rectangle perimeter.

        Args:
            rectangle: Rectangle to calculate.

        Returns:
            Perimeter description.
        """
        perimeter = 2 * (rectangle.width + rectangle.height)
        return f"Rectangle perimeter: {perimeter:.2f}"

    def visit_triangle(self, triangle: Triangle) -> str:
        """Calculate triangle perimeter (assumes right triangle).

        Args:
            triangle: Triangle to calculate.

        Returns:
            Perimeter description.
        """
        import math
        hypotenuse = math.sqrt(triangle.base**2 + triangle.height**2)
        perimeter = triangle.base + triangle.height + hypotenuse
        return f"Triangle perimeter: {perimeter:.2f}"


class XMLExporter(ShapeVisitor):
    """Visitor that exports shapes to XML format."""

    def visit_circle(self, circle: Circle) -> str:
        """Export circle to XML.

        Args:
            circle: Circle to export.

        Returns:
            XML representation.
        """
        return f'<Circle radius="{circle.radius}"/>'

    def visit_rectangle(self, rectangle: Rectangle) -> str:
        """Export rectangle to XML.

        Args:
            rectangle: Rectangle to export.

        Returns:
            XML representation.
        """
        return f'<Rectangle width="{rectangle.width}" height="{rectangle.height}"/>'

    def visit_triangle(self, triangle: Triangle) -> str:
        """Export triangle to XML.

        Args:
            triangle: Triangle to export.

        Returns:
            XML representation.
        """
        return f'<Triangle base="{triangle.base}" height="{triangle.height}"/>'


class JSONExporter(ShapeVisitor):
    """Visitor that exports shapes to JSON format."""

    def visit_circle(self, circle: Circle) -> str:
        """Export circle to JSON.

        Args:
            circle: Circle to export.

        Returns:
            JSON representation.
        """
        return f'{{"type": "circle", "radius": {circle.radius}}}'

    def visit_rectangle(self, rectangle: Rectangle) -> str:
        """Export rectangle to JSON.

        Args:
            rectangle: Rectangle to export.

        Returns:
            JSON representation.
        """
        return f'{{"type": "rectangle", "width": {rectangle.width}, "height": {rectangle.height}}}'

    def visit_triangle(self, triangle: Triangle) -> str:
        """Export triangle to JSON.

        Args:
            triangle: Triangle to export.

        Returns:
            JSON representation.
        """
        return f'{{"type": "triangle", "base": {triangle.base}, "height": {triangle.height}}}'


class ShapeCollection:
    """Collection of shapes that can be visited."""

    def __init__(self) -> None:
        """Initialize empty shape collection."""
        self.shapes: list[Shape] = []

    def add_shape(self, shape: Shape) -> None:
        """Add a shape to the collection.

        Args:
            shape: Shape to add.
        """
        self.shapes.append(shape)

    def accept_all(self, visitor: ShapeVisitor) -> list[str]:
        """Apply visitor to all shapes.

        Args:
            visitor: Visitor to apply.

        Returns:
            List of results from visiting each shape.
        """
        return [shape.accept(visitor) for shape in self.shapes]
