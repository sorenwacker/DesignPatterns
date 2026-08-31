# Factory Pattern

**Category:** Creational Pattern

## Overview

Define an interface for creating objects, but let subclasses or factory methods decide which class to instantiate. This pattern encapsulates object creation logic, making it easier to manage and modify instantiation without coupling code to specific classes.

## Usage Guidelines

**Use when:**

- Multiple related types exist with a common interface and instances need to be created based on runtime conditions
- Object creation requires configuration, validation, or complex initialization logic
- Client code should be decoupled from concrete class implementations
- You need to easily substitute mock objects during testing

**Avoid when:**

- Creating objects is straightforward with no special logic required
- Only one class needs to be instantiated
- The added indirection doesn't provide meaningful benefits
- Performance overhead is unacceptable for critical operations

## Implementation

```python
from design_patterns.structural.inheritance import Animal, Cat, Dog


class AnimalFactory:
    """Factory class to create Animal instances."""

    def get_animal(self, animal_type: str, name: str) -> Animal:
        """Creates an instance of Animal based on the provided type.

        Args:
            animal_type (str): The type of animal to create ('dog' or 'cat').
            name (str): The name of the animal.

        Returns:
            Animal: An instance of Dog or Cat.

        Raises:
            ValueError: If the animal_type is not 'dog' or 'cat'.
        """
        if animal_type == "dog":
            return Dog(name)
        if animal_type == "cat":
            return Cat(name)
        msg = f"Unknown animal type: {animal_type}"
        raise ValueError(msg)
```

The products come from `design_patterns.structural.inheritance`: `Animal` is an abstract base with an abstract `speak`, and `Dog` and `Cat` are its concrete subclasses. The factory is the only place that maps a string to a concrete class, so callers never name `Dog` or `Cat` themselves.

### Usage

```python
# Create factory
factory = AnimalFactory()

# Create different animals using the factory
dog = factory.get_animal("dog", "Buddy")
cat = factory.get_animal("cat", "Whiskers")

print(dog.speak())  # Output: Buddy says woof!
print(cat.speak())  # Output: Whiskers says meow!
```

## Trade-offs

**Benefits:**

1. Encapsulation of object creation logic, hidden from clients
2. Easy to add new product types without modifying client code
3. Loose coupling through dependency on interfaces rather than concrete classes
4. Single Responsibility Principle by separating creation from business logic

**Drawbacks:**

1. Increased complexity through additional classes and indirection
2. Factory can become large with many product types
3. Changing the factory interface affects all clients
4. Limited flexibility as simple factories create only one type at a time

## Real-World Examples

- Database connections based on configuration
- Document parsers based on file type
- Platform-specific UI elements
- Logger implementations (file, console, remote)

## Related Patterns

- Abstract Factory
- Builder
- Prototype
- Singleton

## API Reference

::: design_patterns.creational.factory
    options:
      show_root_heading: true
      show_source: true
