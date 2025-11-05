"""Tests for the Visitor pattern."""

from design_patterns.behavioral.visitor import (
    AreaCalculator,
    Circle,
    JSONExporter,
    PerimeterCalculator,
    Rectangle,
    ShapeCollection,
    Triangle,
    XMLExporter,
)


def test_circle_area():
    """Test calculating circle area."""
    circle = Circle(5)
    calculator = AreaCalculator()
    result = circle.accept(calculator)

    assert "Circle area" in result
    assert "78.54" in result


def test_rectangle_area():
    """Test calculating rectangle area."""
    rectangle = Rectangle(4, 6)
    calculator = AreaCalculator()
    result = rectangle.accept(calculator)

    assert "Rectangle area" in result
    assert "24.00" in result


def test_triangle_area():
    """Test calculating triangle area."""
    triangle = Triangle(10, 5)
    calculator = AreaCalculator()
    result = triangle.accept(calculator)

    assert "Triangle area" in result
    assert "25.00" in result


def test_circle_perimeter():
    """Test calculating circle perimeter."""
    circle = Circle(5)
    calculator = PerimeterCalculator()
    result = circle.accept(calculator)

    assert "Circle perimeter" in result
    assert "31.42" in result


def test_rectangle_perimeter():
    """Test calculating rectangle perimeter."""
    rectangle = Rectangle(4, 6)
    calculator = PerimeterCalculator()
    result = rectangle.accept(calculator)

    assert "Rectangle perimeter" in result
    assert "20.00" in result


def test_triangle_perimeter():
    """Test calculating triangle perimeter."""
    triangle = Triangle(3, 4)
    calculator = PerimeterCalculator()
    result = triangle.accept(calculator)

    assert "Triangle perimeter" in result
    assert "12.00" in result


def test_xml_export_circle():
    """Test exporting circle to XML."""
    circle = Circle(5)
    exporter = XMLExporter()
    result = circle.accept(exporter)

    assert result == '<Circle radius="5"/>'


def test_xml_export_rectangle():
    """Test exporting rectangle to XML."""
    rectangle = Rectangle(4, 6)
    exporter = XMLExporter()
    result = rectangle.accept(exporter)

    assert result == '<Rectangle width="4" height="6"/>'


def test_xml_export_triangle():
    """Test exporting triangle to XML."""
    triangle = Triangle(10, 5)
    exporter = XMLExporter()
    result = triangle.accept(exporter)

    assert result == '<Triangle base="10" height="5"/>'


def test_json_export_circle():
    """Test exporting circle to JSON."""
    circle = Circle(5)
    exporter = JSONExporter()
    result = circle.accept(exporter)

    assert '"type": "circle"' in result
    assert '"radius": 5' in result


def test_json_export_rectangle():
    """Test exporting rectangle to JSON."""
    rectangle = Rectangle(4, 6)
    exporter = JSONExporter()
    result = rectangle.accept(exporter)

    assert '"type": "rectangle"' in result
    assert '"width": 4' in result
    assert '"height": 6' in result


def test_json_export_triangle():
    """Test exporting triangle to JSON."""
    triangle = Triangle(10, 5)
    exporter = JSONExporter()
    result = triangle.accept(exporter)

    assert '"type": "triangle"' in result
    assert '"base": 10' in result
    assert '"height": 5' in result


def test_multiple_visitors_on_same_shape():
    """Test that multiple visitors can operate on the same shape."""
    circle = Circle(5)

    area = circle.accept(AreaCalculator())
    perimeter = circle.accept(PerimeterCalculator())
    xml = circle.accept(XMLExporter())

    assert "area" in area.lower()
    assert "perimeter" in perimeter.lower()
    assert "Circle" in xml


def test_shape_collection():
    """Test visiting all shapes in a collection."""
    collection = ShapeCollection()
    collection.add_shape(Circle(5))
    collection.add_shape(Rectangle(4, 6))
    collection.add_shape(Triangle(10, 5))

    results = collection.accept_all(AreaCalculator())

    assert len(results) == 3
    assert any("Circle area" in r for r in results)
    assert any("Rectangle area" in r for r in results)
    assert any("Triangle area" in r for r in results)


def test_shape_collection_xml_export():
    """Test exporting all shapes in collection to XML."""
    collection = ShapeCollection()
    collection.add_shape(Circle(3))
    collection.add_shape(Rectangle(2, 4))

    results = collection.accept_all(XMLExporter())

    assert len(results) == 2
    assert '<Circle radius="3"/>' in results
    assert '<Rectangle width="2" height="4"/>' in results


def test_visitor_pattern_extensibility():
    """Test that new visitors can be added without modifying shapes."""
    circle = Circle(5)
    rectangle = Rectangle(4, 6)

    # Can use existing visitors
    area_calc = AreaCalculator()
    perim_calc = PerimeterCalculator()
    xml_exp = XMLExporter()
    json_exp = JSONExporter()

    # All visitors work with all shapes
    visitors = [area_calc, perim_calc, xml_exp, json_exp]
    shapes = [circle, rectangle]

    for shape in shapes:
        for visitor in visitors:
            result = shape.accept(visitor)
            assert isinstance(result, str)
            assert len(result) > 0


def test_empty_shape_collection():
    """Test visiting empty shape collection."""
    collection = ShapeCollection()
    results = collection.accept_all(AreaCalculator())

    assert results == []
