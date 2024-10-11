"""Composite Pattern Example

This module demonstrates the Composite design pattern in Python 
using a base class `Shape`, along with concrete implementations 
`Circle` and `Rectangle`. The `CompositeShape` class allows 
for grouping of multiple shapes, enabling a unified interface 
to draw them collectively.

Example:
    ```
    circle = Circle()
    rectangle = Rectangle()
    composite = CompositeShape()
    composite.add(circle)
    composite.add(rectangle)
    print(composite.draw())  # Output: Composite Shape: Drawing a circle., Drawing a rectangle.
    ```

"""

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
            shape (Shape): The shape to be added.
        """
        self.shapes.append(shape)

    def draw(self) -> str:
        """Draws all shapes in the composite shape.

        Returns:
            str: A string representation of all drawn shapes.
        """
        return "Composite Shape: " + ", ".join(shape.draw() for shape in self.shapes)

