# Design Patterns in Python

Python implementation of the 23 Gang of Four design patterns with type hints and comprehensive examples.

## Getting Started

Explore patterns by category using the sidebar navigation:

- **Creational** (5) - Object creation mechanisms
- **Behavioral** (11) - Object interaction and responsibility
- **Structural** (7) - Object composition and relationships

## Quick Links

- [Introduction](introduction.md) - Core concepts and principles
- [Pattern Catalog](overview.md) - Complete pattern reference table
- [Pattern Selection Guide](pattern_guide.md) - Choosing the right pattern
- [Quick Reference](quick_reference.md) - Pattern cheat sheet

## Installation

```bash
pip install -e .
```

## Usage

```python
from design_patterns.creational.factory import AnimalFactory
from design_patterns.behavioral.strategy import ShoppingCart, CreditCardPayment

factory = AnimalFactory()
dog = factory.get_animal("dog", "Buddy")

cart = ShoppingCart()
cart.set_payment_strategy(CreditCardPayment("1234-5678"))
```
