# Interpreter Pattern

**Category:** Behavioral Pattern

## Intent

Define a representation for a grammar along with an interpreter that uses the representation to interpret sentences in the language. The Interpreter pattern is used to evaluate sentences in a language by representing grammar rules as classes and interpreting expressions recursively.

## Problem

When you need to evaluate expressions or implement a simple language, hard-coding the logic leads to:

- Inflexible parsing and evaluation
- Difficulty modifying grammar rules
- Complex conditional logic for expression evaluation
- Hard to extend with new expressions
- Tight coupling between grammar and evaluation logic

## When to Use

Use the Interpreter pattern when:

- **Simple grammar**: Grammar is simple and well-defined
- **Efficiency not critical**: Performance is not a primary concern
- **Frequent changes**: Grammar changes frequently
- **Expression evaluation**: Need to evaluate expressions in a language
- **Rule engines**: Implementing business rule engines
- **Query languages**: Building simple query or filtering languages
- **Configuration parsing**: Parsing and evaluating configuration expressions

## When NOT to Use

Avoid the Interpreter pattern when:

- **Complex grammar**: Grammar is complex (use parser generators instead)
- **Performance critical**: Interpretation overhead is unacceptable
- **Compiled better**: Compilation to bytecode would be more efficient
- **Standard parsers available**: Existing parsing libraries suffice
- **Large language**: Language has many grammar rules

## Structure

The Interpreter pattern involves:

- **Abstract Expression**: Interface for interpreting expressions
- **Terminal Expression**: Implements interpretation for terminal symbols
- **Non-terminal Expression**: Implements interpretation for grammar rules
- **Context**: Contains global information for interpretation
- **Client**: Builds abstract syntax tree and initiates interpretation

## Implementation

### Boolean Expression Interpreter

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

## Usage Example

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
print(is_leadership.interpret("Director of Engineering"))  # True
print(is_leadership.interpret("Software Engineer"))  # False
```

## Key Benefits

1. **Extensibility**: Easy to add new grammar rules
2. **Separation of concerns**: Grammar and interpretation are separate
3. **Flexibility**: Grammar can be modified by composing expressions
4. **Explicit grammar**: Grammar rules are represented as classes
5. **Reusability**: Expression objects can be reused

## Drawbacks

1. **Class proliferation**: Many classes for complex grammars
2. **Performance**: Interpretation is slower than compiled alternatives
3. **Complexity**: Complex grammars lead to complex class hierarchies
4. **Maintenance**: Large grammars are hard to maintain
5. **Limited scalability**: Not suitable for complex languages

## Real-World Examples

- **SQL interpreters**: Parsing and executing SQL queries
- **Regular expressions**: Pattern matching engines
- **Mathematical expressions**: Evaluating arithmetic expressions
- **Business rule engines**: Evaluating business rules
- **Configuration languages**: Parsing configuration files
- **Search queries**: Interpreting search syntax
- **Scripting languages**: Simple embedded scripting

## Related Patterns

- **Composite**: Interpreter uses Composite for expression trees
- **Flyweight**: Can share terminal symbols
- **Iterator**: Can iterate through expression tree
- **Visitor**: Can process expression trees

## API Reference

::: design_patterns.behavioral.interpreter
    options:
      show_root_heading: true
      show_source: true
