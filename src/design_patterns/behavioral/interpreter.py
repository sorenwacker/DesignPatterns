"""Interpreter Pattern Module

The Interpreter pattern represents a grammar as a class hierarchy and an
operation that evaluates sentences of that grammar. Here the grammar is
boolean search: a terminal expression matches a literal inside a context
string, and the non-terminal expressions combine matches with AND and OR.

Example:
    ```
    john = TerminalExpression("John")
    doe = TerminalExpression("Doe")
    is_john_doe = AndExpression(john, doe)

    is_john_doe.interpret("John Doe")  # True
    is_john_doe.interpret("John Smith")  # False
    ```
"""

from abc import ABC, abstractmethod


class Expression(ABC):
    """Base class for interpreting expressions in a given context."""

    @abstractmethod
    def interpret(self, context: str) -> bool:
        """Interpret the given context.

        Args:
            context (str): The input context to interpret.

        Returns:
            bool: The result of the interpretation.
        """


class TerminalExpression(Expression):
    """Terminal expression that checks for a literal value."""

    def __init__(self, literal: str) -> None:
        """Record the literal to look for.

        Args:
            literal: The text that must appear in the context.
        """
        self.literal = literal

    def interpret(self, context: str) -> bool:
        """Check if the context contains the literal."""
        return self.literal in context


class OrExpression(Expression):
    """Non-terminal expression for logical OR."""

    def __init__(self, expr1: Expression, expr2: Expression) -> None:
        """Combine two expressions.

        Args:
            expr1: The first operand.
            expr2: The second operand.
        """
        self.expr1 = expr1
        self.expr2 = expr2

    def interpret(self, context: str) -> bool:
        """Return true if either expression is true."""
        return self.expr1.interpret(context) or self.expr2.interpret(context)


class AndExpression(Expression):
    """Non-terminal expression for logical AND."""

    def __init__(self, expr1: Expression, expr2: Expression) -> None:
        """Combine two expressions.

        Args:
            expr1: The first operand.
            expr2: The second operand.
        """
        self.expr1 = expr1
        self.expr2 = expr2

    def interpret(self, context: str) -> bool:
        """Return true if both expressions are true."""
        return self.expr1.interpret(context) and self.expr2.interpret(context)
