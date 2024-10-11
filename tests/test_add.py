import pytest

from design_patterns import add

def test_add__two_integers():
    expected = 5
    result = add(2, 3)
    assert result == expected, f"Expected {expected}, but got {result}."

def test_add__negative_values():
    expected = -20
    result = add(-12, -8)
    assert result == expected, f"Expected {expected}, but got {result}."

def test_add__zeros():
    expected = 0
    result = add(0, 0)
    assert result == expected, f"Expected {expected}, but got {result}."

def test_add__floats_raise_ValueError():
    with pytest.raises(ValueError, match="Both arguments must be integers"):
        add(0.8, 0.4)