# Design Patterns in Python

A library demonstrating the 23 Gang of Four design patterns implemented in Python with modern idioms and type hints.

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

- [Pattern Selection Guide](docs/pattern_guide.md)
- [Pattern Comparison Guide](docs/pattern_comparison.md)
- [Practical Examples](docs/practical_examples.md)
- [Anti-Patterns](docs/anti_patterns.md)
- [Quick Reference](docs/quick_reference.md)

## Installation

```bash
# Using uv (recommended)
uv pip install -e .

# Using pip
pip install -e .
```

## Usage

Run examples:
```bash
python examples/factory_logger.py
python examples/strategy_payment.py
```

Use in code:
```python
from design_patterns.creational.factory import AnimalFactory
from design_patterns.behavioral.strategy import ShoppingCart, CreditCardPayment

factory = AnimalFactory()
dog = factory.get_animal("dog", "Buddy")

cart = ShoppingCart()
cart.set_payment_strategy(CreditCardPayment("1234-5678"))
```

## Development

Run tests:
```bash
pytest
```

Generate documentation locally:
```bash
mkdocs serve
```

## License

MIT License - see [LICENSE](LICENSE).
