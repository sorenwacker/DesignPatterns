"""Tests for the Interpreter pattern."""

from design_patterns.behavioral.interpreter import (
    AndExpression,
    OrExpression,
    TerminalExpression,
)


def test_terminal_expression_found():
    """Test that TerminalExpression finds literal in context."""
    expr = TerminalExpression("Hello")
    assert expr.interpret("Hello World") is True


def test_terminal_expression_not_found():
    """Test that TerminalExpression doesn't find missing literal."""
    expr = TerminalExpression("Goodbye")
    assert expr.interpret("Hello World") is False


def test_or_expression_first_true():
    """Test OrExpression when first expression is true."""
    expr1 = TerminalExpression("Hello")
    expr2 = TerminalExpression("Goodbye")
    or_expr = OrExpression(expr1, expr2)
    assert or_expr.interpret("Hello World") is True


def test_or_expression_second_true():
    """Test OrExpression when second expression is true."""
    expr1 = TerminalExpression("Goodbye")
    expr2 = TerminalExpression("World")
    or_expr = OrExpression(expr1, expr2)
    assert or_expr.interpret("Hello World") is True


def test_or_expression_both_false():
    """Test OrExpression when both expressions are false."""
    expr1 = TerminalExpression("Goodbye")
    expr2 = TerminalExpression("Universe")
    or_expr = OrExpression(expr1, expr2)
    assert or_expr.interpret("Hello World") is False


def test_and_expression_both_true():
    """Test AndExpression when both expressions are true."""
    expr1 = TerminalExpression("Hello")
    expr2 = TerminalExpression("World")
    and_expr = AndExpression(expr1, expr2)
    assert and_expr.interpret("Hello World") is True


def test_and_expression_first_false():
    """Test AndExpression when first expression is false."""
    expr1 = TerminalExpression("Goodbye")
    expr2 = TerminalExpression("World")
    and_expr = AndExpression(expr1, expr2)
    assert and_expr.interpret("Hello World") is False


def test_and_expression_second_false():
    """Test AndExpression when second expression is false."""
    expr1 = TerminalExpression("Hello")
    expr2 = TerminalExpression("Universe")
    and_expr = AndExpression(expr1, expr2)
    assert and_expr.interpret("Hello World") is False


def test_complex_expression():
    """Test complex nested expression (John OR Jane) AND Doe."""
    john = TerminalExpression("John")
    jane = TerminalExpression("Jane")
    doe = TerminalExpression("Doe")

    john_or_jane = OrExpression(john, jane)
    full_name = AndExpression(john_or_jane, doe)

    assert full_name.interpret("John Doe") is True
    assert full_name.interpret("Jane Doe") is True
    assert full_name.interpret("John Smith") is False
    assert full_name.interpret("Bob Doe") is False
