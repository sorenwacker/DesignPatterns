# Decorator Pattern

**Category:** Structural Pattern

## Intent

Attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality, allowing behavior to be added to individual objects without affecting other objects of the same class.

## Problem

When you need to add functionality to objects, traditional inheritance creates rigid structures that lead to:

- Explosion of subclasses for every combination of features
- Static behavior defined at compile time
- Inability to combine features flexibly
- Modification of existing classes when adding new features

## When to Use

Use the Decorator pattern when:

- **Dynamic behavior**: You need to add responsibilities to objects at runtime
- **Reversible enhancements**: Features should be added and removed dynamically
- **Combination flexibility**: You want to combine features in various ways
- **Extension without modification**: Existing classes should remain unchanged (Open/Closed Principle)
- **Multiple orthogonal features**: Features are independent and can be combined arbitrarily
- **Alternative to subclassing**: Subclassing would create too many classes or isn't feasible

## When NOT to Use

Avoid the Decorator pattern when:

- **Static behavior**: All behavior is known at compile time and doesn't change
- **Simple enhancements**: A single subclass would suffice
- **Order matters**: The order of applying decorators significantly affects behavior and causes confusion
- **Identity checks**: Code relies on object type checking (decorators change object identity)
- **Performance critical**: Multiple wrapper layers introduce unacceptable overhead
- **Few combinations**: Limited feature combinations don't justify the pattern

## Structure

The Decorator pattern involves:

- **Component Interface**: Defines interface for objects that can have responsibilities added
- **Concrete Component**: Defines base object to which responsibilities can be attached
- **Decorator**: Maintains reference to a Component and conforms to Component interface
- **Concrete Decorators**: Add responsibilities to the component

## Implementation

### Coffee Shop Example

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

### Usage Example

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

### Data Source Example

```python
from abc import ABC, abstractmethod

class DataSource(ABC):
    @abstractmethod
    def write_data(self, data: str) -> None:
        pass

    @abstractmethod
    def read_data(self) -> str:
        pass

class FileDataSource(DataSource):
    def __init__(self, filename: str):
        self.filename = filename
        self._data: str = ""

    def write_data(self, data: str) -> None:
        self._data = data

    def read_data(self) -> str:
        return self._data

class EncryptionDecorator(DataSource):
    def __init__(self, source: DataSource):
        self._source = source

    def write_data(self, data: str) -> None:
        encrypted = data[::-1]  # Simple encryption
        self._source.write_data(encrypted)

    def read_data(self) -> str:
        encrypted = self._source.read_data()
        return encrypted[::-1]  # Decrypt

class CompressionDecorator(DataSource):
    def __init__(self, source: DataSource):
        self._source = source

    def write_data(self, data: str) -> None:
        compressed = f"[COMPRESSED]{data}"
        self._source.write_data(compressed)

    def read_data(self) -> str:
        data = self._source.read_data()
        if data.startswith("[COMPRESSED]"):
            return data[12:]
        return data

# Usage: Combine encryption and compression
source = FileDataSource("data.txt")
source = EncryptionDecorator(source)
source = CompressionDecorator(source)

source.write_data("Hello, World!")
print(source.read_data())  # Output: Hello, World!
```

## Key Benefits

1. **Flexibility**: Add or remove responsibilities at runtime
2. **Open/Closed Principle**: Extend functionality without modifying existing code
3. **Single Responsibility**: Each decorator focuses on one concern
4. **Composability**: Mix and match decorators for different combinations
5. **Alternative to inheritance**: Avoids class explosion from multiple features
6. **Incremental enhancement**: Add features gradually as needed

## Drawbacks

1. **Complexity**: Many small objects and layers can be hard to understand
2. **Order dependency**: Decorator order may matter, causing confusion
3. **Identity issues**: Decorated objects differ from original objects
4. **Debugging difficulty**: Stack traces show multiple wrapper layers
5. **Initialization complexity**: Setting up decorated objects can be verbose
6. **Interface explosion**: All features must be in the base interface

## Real-World Examples

- **I/O streams**: BufferedInputStream, GZIPInputStream wrap basic streams
- **GUI components**: Adding scrollbars, borders to UI elements
- **Middleware**: Adding logging, authentication, caching to HTTP handlers
- **Text formatting**: Adding bold, italic, underline to text
- **Caching layers**: Adding caching to database or API calls
- **Notification systems**: Adding email, SMS, push notification layers

## Related Patterns

- **Adapter**: Changes interface vs adding responsibilities
- **Composite**: Aggregates objects vs adding behavior
- **Proxy**: Controls access vs enhancing functionality
- **Strategy**: Changes algorithm vs adding features
- **Chain of Responsibility**: Passes requests vs transforming them

## API Reference

::: design_patterns.structural.decorator
    options:
      show_root_heading: true
      show_source: true
