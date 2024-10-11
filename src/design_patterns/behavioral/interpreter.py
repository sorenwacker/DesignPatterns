class Expression:
    """Base class for interpreting expressions in a given context."""

    def interpret(self, context: str) -> bool:
        """
        Interpret the given context.

        Args:
            context (str): The input context to interpret.

        Returns:
            bool: The result of the interpretation.
        """
        pass


class TerminalExpression(Expression):
    """Terminal expression that checks for a literal value."""

    def __init__(self, literal: str) -> None:
        self.literal = literal

    def interpret(self, context: str) -> bool:
        """Check if the context contains the literal."""
        return self.literal in context


class OrExpression(Expression):
    """Non-terminal expression for logical OR."""

    def __init__(self, expr1: Expression, expr2: Expression) -> None:
        self.expr1 = expr1
        self.expr2 = expr2

    def interpret(self, context: str) -> bool:
        """Return true if either expression is true."""
        return self.expr1.interpret(context) or self.expr2.interpret(context)


class AndExpression(Expression):
    """Non-terminal expression for logical AND."""

    def __init__(self, expr1: Expression, expr2: Expression) -> None:
        self.expr1 = expr1
        self.expr2 = expr2

    def interpret(self, context: str) -> bool:
        """Return true if both expressions are true."""
        return self.expr1.interpret(context) and self.expr2.interpret(context)



if __name__ == "__main__":
    john = TerminalExpression("John")
    doe = TerminalExpression("Doe")
    is_john_doe = AndExpression(john, doe)

    print(is_john_doe.interpret("John Doe"))  # True
    print(is_john_doe.interpret("John Smith"))  # False
