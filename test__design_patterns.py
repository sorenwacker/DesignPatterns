"""Tests for the design_patterns"""

import pytest

from design_patterns import add, divide

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

def test_divide__two_integers():
    numerator = 10
    denominator = 2
    expected = 5.0
    result = divide(numerator, denominator)
    assert result == expected, f"Expected {expected}, but got {result}."

def test_divide__float_and_integer():
    numerator = 10.5
    denominator = 2
    expected = 5.25
    result = divide(numerator, denominator)
    assert result == expected, f"Expected {expected}, but got {result}."

def test_divide__integer_and_float():
    numerator = 10
    denominator = 2.5
    expected = 4.0
    result = divide(numerator, denominator)
    assert result == expected, f"Expected {expected}, but got {result}."

def test_divide__denominator_zero_raises_ValueError():
    numerator = 9
    denominator = 0
    with pytest.raises(ValueError, match="Denominator cannot be zero"):
        divide(numerator, denominator)

def test_divide__numerator_zero():
    numerator = 0
    denominator = 5
    expected = 0.0
    result = divide(numerator, denominator)
    assert result == expected, f"Expected {expected}, but got {result}."

def test_divide__negative_values():
    numerator = -10
    denominator = 2
    expected = -5.0
    result = divide(numerator, denominator)
    assert result == expected, f"Expected {expected}, but got {result}."
