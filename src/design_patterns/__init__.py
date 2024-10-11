#src/design_patterns/__init__.py

"""
This package demonstrates various software design patterns implemented in Python.
It provides practical examples and explanations of common design patterns to help
developers understand and apply these patterns in their own projects.
"""


from __future__ import annotations

from importlib.metadata import version

__all__ = ("__version__",)
__version__ = version(__name__)


def add(a: int, b: int) -> int:
    """
    Adds two numbers together.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        sum: The sum of the two numbers.

    Raises:
        ValueError: If either a or b is not an integer.
        
    Examples:
        >>> add(1, 2)
        3
        >>> add(-1, 1)
        0
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError("Both arguments must be integers")
    return a + b


def divide(numerator: float, denominator: float) -> float:
    """
    Divides the numerator by the denominator.

    Args:
        numerator (float or int): The number to be divided.
        denominator (float or int): The number by which to divide.

    Returns:
        float: The result of the division.

    Raises:
        ValueError: If the denominator is zero.

    Examples:
        >>> divide(6, 2)
        3.0
        >>> divide(7, 3)
        2.3333333333333335
    """
    if denominator == 0:
        raise ValueError("Denominator cannot be zero")
    
    # Cast both to float before division
    return float(numerator) / float(denominator)



if __name__ == "__main__":
    import doctest
    doctest.testmod()