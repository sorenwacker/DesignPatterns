# Interpreter Pattern

**Category:** Behavioral Pattern

## Overview

Define a representation for a grammar along with an interpreter that uses the representation to interpret sentences in the language. This pattern is used to evaluate sentences by representing grammar rules as classes and interpreting expressions recursively.

## Usage Guidelines

**Use when:**

- Grammar is simple and well-defined
- Efficiency is not a primary concern
- Need to evaluate expressions in a language
- Implementing simple business rule engines

**Avoid when:**

- Grammar is complex (use parser generators instead)
- Performance is critical as interpretation adds overhead
- Compilation to bytecode would be more efficient
- Standard parsing libraries suffice

## Implementation

```python
class Expression:
    """Base class for interpreting expressions in a given context."""

    def interpret(self, context: str) -> bool:
        """Interpret the given context.

        Args:
            context: The input context to interpret.

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
```

### Usage

```python
# Build expression: "John" AND "Doe"
john = TerminalExpression("John")
doe = TerminalExpression("Doe")
is_john_doe = AndExpression(john, doe)

print(is_john_doe.interpret("John Doe"))  # True
print(is_john_doe.interpret("John Smith"))  # False

# Build expression: "Manager" OR "Director"
manager = TerminalExpression("Manager")
director = TerminalExpression("Director")
is_leadership = OrExpression(manager, director)

print(is_leadership.interpret("Senior Manager"))  # True
print(is_leadership.interpret("Software Engineer"))  # False
```

## Trade-offs

**Benefits:**

1. Easy to add new grammar rules through extensibility
2. Grammar and interpretation are separate concerns
3. Grammar can be modified by composing expressions
4. Expression objects can be reused

**Drawbacks:**

1. Many classes for complex grammars causing class proliferation
2. Interpretation is slower than compiled alternatives
3. Complex grammars lead to complex class hierarchies
4. Large grammars are hard to maintain

## Real-World Examples

- SQL interpreters parsing and executing queries
- Regular expressions for pattern matching
- Mathematical expressions evaluation
- Business rule engines

## Related Patterns

- Composite
- Flyweight
- Iterator
- Visitor

## API Reference

::: design_patterns.behavioral.interpreter
    options:
      show_root_heading: true
      show_source: true
