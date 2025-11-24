# Decorator Pattern

**Category:** Structural Pattern

## Overview

Attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality, allowing behavior to be added to individual objects without affecting other objects of the same class.

## Usage Guidelines

**Use when:**
- Need to add responsibilities to objects at runtime
- Features should be added and removed dynamically
- Want to combine features in various ways
- Existing classes should remain unchanged (Open/Closed Principle)

**Avoid when:**
- All behavior is known at compile time and doesn't change
- A single subclass would suffice for simple enhancements
- The order of applying decorators significantly affects behavior and causes confusion
- Multiple wrapper layers introduce unacceptable performance overhead

## Implementation

```python
from abc import ABC, abstractmethod

# Component Interface
class Coffee(ABC):
    @abstractmethod
    def get_cost(self) -> float:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

# Concrete Component
class SimpleCoffee(Coffee):
    def get_cost(self) -> float:
        return 1.0

    def get_description(self) -> str:
        return "Simple Coffee"

# Base Decorator
class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    def get_cost(self) -> float:
        return self._coffee.get_cost()

    def get_description(self) -> str:
        return self._coffee.get_description()

# Concrete Decorators
class MilkDecorator(CoffeeDecorator):
    def get_cost(self) -> float:
        return self._coffee.get_cost() + 0.5

    def get_description(self) -> str:
        return self._coffee.get_description() + ", Milk"

class SugarDecorator(CoffeeDecorator):
    def get_cost(self) -> float:
        return self._coffee.get_cost() + 0.2

    def get_description(self) -> str:
        return self._coffee.get_description() + ", Sugar"

class VanillaDecorator(CoffeeDecorator):
    def get_cost(self) -> float:
        return self._coffee.get_cost() + 0.7

    def get_description(self) -> str:
        return self._coffee.get_description() + ", Vanilla"
```

### Usage

```python
# Start with simple coffee
coffee = SimpleCoffee()
print(f"{coffee.get_description()}: ${coffee.get_cost():.2f}")
# Output: Simple Coffee: $1.00

# Add milk
coffee = MilkDecorator(coffee)
print(f"{coffee.get_description()}: ${coffee.get_cost():.2f}")
# Output: Simple Coffee, Milk: $1.50

# Add sugar
coffee = SugarDecorator(coffee)
print(f"{coffee.get_description()}: ${coffee.get_cost():.2f}")
# Output: Simple Coffee, Milk, Sugar: $1.70

# Add vanilla
coffee = VanillaDecorator(coffee)
print(f"{coffee.get_description()}: ${coffee.get_cost():.2f}")
# Output: Simple Coffee, Milk, Sugar, Vanilla: $2.40
```

## Trade-offs

**Benefits:**
1. Add or remove responsibilities at runtime for flexibility
2. Extend functionality without modifying existing code (Open/Closed Principle)
3. Each decorator focuses on one concern (Single Responsibility)
4. Mix and match decorators for different combinations

**Drawbacks:**
1. Many small objects and layers can be hard to understand
2. Decorator order may matter, causing confusion
3. Decorated objects differ from original objects causing identity issues
4. Stack traces show multiple wrapper layers making debugging difficult

## Real-World Examples

- I/O streams with BufferedInputStream, GZIPInputStream wrapping basic streams
- GUI components adding scrollbars, borders to UI elements
- Middleware adding logging, authentication, caching to HTTP handlers
- Caching layers adding caching to database or API calls

## Related Patterns

- Adapter
- Composite
- Proxy
- Strategy
- Chain of Responsibility

## API Reference

::: design_patterns.structural.decorator
    options:
      show_root_heading: true
      show_source: true
