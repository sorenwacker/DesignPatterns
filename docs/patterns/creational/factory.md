# Factory Pattern

**Category:** Creational Pattern

## Intent

Define an interface for creating objects, but let subclasses or factory methods decide which class to instantiate. The Factory pattern encapsulates object creation logic, making it easier to manage and modify object instantiation.

## Problem

Creating objects directly using constructors couples your code to specific classes, making it difficult to:

- Change which classes are instantiated
- Add new types without modifying existing code
- Centralize and control object creation logic
- Handle complex creation scenarios

## When to Use

Use the Factory pattern when:

- **Multiple related types**: You have multiple classes implementing a common interface and need to create instances based on runtime conditions
- **Centralized creation logic**: Object creation requires configuration, validation, or complex initialization
- **Decoupling**: You want to decouple client code from concrete class implementations
- **Creation variations**: The creation process needs to be customized or extended
- **Testing**: You need to easily substitute mock objects during testing

## When NOT to Use

Avoid the Factory pattern when:

- **Simple instantiation**: Creating objects is straightforward with no special logic required
- **Single type**: Only one class needs to be instantiated
- **Unnecessary abstraction**: The added indirection doesn't provide meaningful benefits
- **Performance critical**: The factory overhead is unacceptable for performance requirements
- **Small codebase**: The pattern adds complexity that isn't justified by the codebase size

## Structure

The Factory pattern involves:

- **Product Interface**: Common interface for all products
- **Concrete Products**: Implementations of the product interface
- **Factory**: Creates and returns product instances based on parameters

## Implementation

### Basic Factory

```python
from abc import ABC, abstractmethod

# Product Interface
class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass

# Concrete Products
class Dog(Animal):
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return f"{self.name} says woof!"

class Cat(Animal):
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return f"{self.name} says meow!"

# Factory
class AnimalFactory:
    def get_animal(self, animal_type: str, name: str) -> Animal:
        if animal_type == "dog":
            return Dog(name)
        elif animal_type == "cat":
            return Cat(name)
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")
```

### Usage Example

```python
# Create factory
factory = AnimalFactory()

# Create different animals using the factory
dog = factory.get_animal("dog", "Buddy")
cat = factory.get_animal("cat", "Whiskers")

print(dog.speak())  # Output: Buddy says woof!
print(cat.speak())  # Output: Whiskers says meow!
```

## Key Benefits

1. **Encapsulation**: Object creation logic is centralized and hidden from clients
2. **Flexibility**: Easy to add new product types without modifying client code
3. **Loose coupling**: Clients depend on interfaces rather than concrete classes
4. **Single Responsibility**: Creation logic is separated from business logic
5. **Open/Closed Principle**: Open for extension (new types) but closed for modification

## Drawbacks

1. **Increased complexity**: Introduces additional classes and indirection
2. **Factory bloat**: Factory can become large with many product types
3. **Rigidity**: Changing the factory interface affects all clients
4. **Limited flexibility**: Simple factories can only create one type of object at a time

## Real-World Examples

- **Database connections**: Creating different database connection objects based on configuration
- **Document parsers**: Instantiating appropriate parser based on file type
- **GUI components**: Creating platform-specific UI elements
- **Logging frameworks**: Creating different logger implementations (file, console, remote)
- **Payment processors**: Creating payment handler based on payment method

## Related Patterns

- **Abstract Factory**: Creates families of related objects
- **Builder**: Constructs complex objects step by step
- **Prototype**: Creates objects by cloning existing instances
- **Singleton**: Ensures only one instance of a class exists

## API Reference

::: design_patterns.creational.factory
    options:
      show_root_heading: true
      show_source: true
