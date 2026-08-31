# Design Patterns in Python

[![Docs](https://github.com/sorenwacker/DesignPatterns/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/sorenwacker/DesignPatterns/actions/workflows/deploy-docs.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Python implementations of 22 of the 23 Gang of Four design patterns (Flyweight is not included), together with testing patterns and gate patterns, with type hints and tests.

## Patterns

### Creational
- Factory - Create objects without specifying exact class
- Singleton - Ensure only one instance exists
- Builder - Construct complex objects step by step
- Prototype - Clone objects instead of creating new ones
- Abstract Factory - Create families of related objects

### Behavioral
- Strategy - Define interchangeable algorithm families
- Observer - Notify dependents of state changes
- Command - Encapsulate requests as objects
- Chain of Responsibility - Pass requests along handler chain
- Interpreter - Interpret language grammar
- State - Alter behavior when internal state changes
- Template Method - Define algorithm skeleton in base class
- Iterator - Access elements sequentially
- Visitor - Separate algorithms from object structure
- Mediator - Reduce coupling between communicating objects
- Memento - Capture and restore object state

### Structural
- Decorator - Add responsibilities dynamically
- Adapter - Make incompatible interfaces work together
- Composite - Treat individual and composed objects uniformly
- Facade - Provide simplified interface to complex subsystem
- Proxy - Control access to another object
- Bridge - Decouple abstraction from implementation
- Composition/Inheritance - Demonstrate OOP principles

## Documentation

Full documentation available at: https://sorenwacker.github.io/DesignPatterns/

- [Introduction](https://sorenwacker.github.io/DesignPatterns/introduction/)
- [Overview](https://sorenwacker.github.io/DesignPatterns/overview/)
- [Design Patterns](https://sorenwacker.github.io/DesignPatterns/)
- [Pattern Selection Guide](https://sorenwacker.github.io/DesignPatterns/pattern_guide/)
- [Pattern Comparison Guide](https://sorenwacker.github.io/DesignPatterns/pattern_comparison/)
- [Practical Examples](https://sorenwacker.github.io/DesignPatterns/practical_examples/)
- [Anti-Patterns](https://sorenwacker.github.io/DesignPatterns/anti_patterns/)
- [Quick Reference](https://sorenwacker.github.io/DesignPatterns/quick_reference/)

## Installation

```bash
uv sync --extra dev
```

## Usage

Run an example:

```bash
uv run python examples/factory_logger.py
```

Use the library in code:

```python
from design_patterns.creational.factory import AnimalFactory
from design_patterns.behavioral.strategy import ShoppingCart, CreditCardPayment

factory = AnimalFactory()
dog = factory.get_animal("dog", "Buddy")

cart = ShoppingCart()
cart.set_payment_strategy(CreditCardPayment("1234-5678"))
```

## Development

`make check` runs every quality gate; `make docs` serves the documentation with hot reload. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full list of gates and the workflow for adding a pattern.

## License

MIT License - see [LICENSE](LICENSE).
