# Project Timeline (Mermaid Gantt Chart)

# Design Patterns in Python

[![Actions Status][actions-badge]][actions-link]
[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

A comprehensive library demonstrating software design patterns implemented in Python, following best practices and modern Python idioms.

## Implemented Patterns

### Creational Patterns (5/5) ✅ Complete
- ✅ Factory - Create objects without specifying exact class
- ✅ Singleton - Ensure only one instance exists
- ✅ Builder - Construct complex objects step by step
- ✅ Prototype - Clone objects instead of creating new ones
- ✅ Abstract Factory - Create families of related objects

### Behavioral Patterns (11/11) ✅ Complete
- ✅ Strategy - Define interchangeable algorithm families
- ✅ Observer - Notify dependents of state changes
- ✅ Command - Encapsulate requests as objects
- ✅ Chain of Responsibility - Pass requests along handler chain
- ✅ Interpreter - Interpret language grammar
- ✅ State - Alter behavior when internal state changes
- ✅ Template Method - Define algorithm skeleton in base class
- ✅ Iterator - Access elements sequentially
- ✅ Visitor - Separate algorithms from object structure
- ✅ Mediator - Reduce coupling between communicating objects
- ✅ Memento - Capture and restore object state

### Structural Patterns (7/7) ✅ Complete
- ✅ Decorator - Add responsibilities dynamically
- ✅ Adapter - Make incompatible interfaces work together
- ✅ Composite - Treat individual and composed objects uniformly
- ✅ Facade - Provide simplified interface to complex subsystem
- ✅ Proxy - Control access to another object
- ✅ Bridge - Decouple abstraction from implementation
- ✅ Composition/Inheritance - Demonstrate OOP principles

## Features

- **100% Complete** - All 23 GoF design patterns implemented
- Modern Python 3.12+ with type hints
- Comprehensive test coverage (275+ tests, 94% coverage)
- Detailed docstrings with usage examples
- mypy type checking configured
- Following Python idioms and best practices
- Multiple real-world examples per pattern
- Benefits, drawbacks, and when (not) to use each pattern documented

## Documentation

Comprehensive guides to help you master design patterns:

- **[Pattern Selection Guide](docs/pattern_guide.md)** - When to use each pattern, benefits, and drawbacks
- **[Pattern Comparison Guide](docs/pattern_comparison.md)** - Compare similar patterns side-by-side
- **[Practical Examples](docs/practical_examples.md)** - Real-world use cases and applications
- **[Anti-Patterns](docs/anti_patterns.md)** - Common mistakes and how to avoid them
- **[Quick Reference](docs/quick_reference.md)** - Cheat sheet for rapid pattern selection

## Installation

Install [pixi](https://pixi.sh):

- Linux and MacOS
    ```bash
    curl -fsSL https://pixi.sh/install.sh | bash
    ```
- Windows (powershell)
    ```bash
    iwr -useb https://pixi.sh/install.ps1 | iex
    ```

Install the dependencies, including the dev dependencies:

```bash
pixi install --all
```

Or install only the runtime dependencies:

```bash
pixi install --environment default
```

Install the package in editable mode:

```bash
uv pip install -e .
```

## Usage

### Running Examples

The `examples/` directory contains practical, runnable demonstrations:

```bash
python examples/factory_logger.py
python examples/strategy_payment.py
python examples/observer_event_system.py
python examples/decorator_middleware.py
python examples/facade_order_system.py
```

### Using in Your Code

```python
from design_patterns.creational.factory import AnimalFactory
from design_patterns.behavioral.strategy import ShoppingCart, CreditCardPayment
from design_patterns.structural.decorator import SimpleCoffee, MilkDecorator

# Factory Pattern
factory = AnimalFactory()
dog = factory.get_animal("dog", "Buddy")

# Strategy Pattern
cart = ShoppingCart()
cart.set_payment_strategy(CreditCardPayment("1234-5678"))

# Decorator Pattern
coffee = MilkDecorator(SimpleCoffee())
```


## Documentation

Generate the documentation locally with

    ```bash
    pixi run -e dev mkdocs serve --watch ./
    ```


## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on how to contribute.

## License

Distributed under the terms of the [MIT license](LICENSE).
