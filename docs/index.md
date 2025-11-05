# Design Patterns in Python

A comprehensive library demonstrating software design patterns implemented in Python, following best practices and modern Python idioms.

## Overview

Design patterns are reusable solutions to commonly occurring problems in software design. This library provides clear, well-tested implementations of the most important design patterns from the Gang of Four (GoF) book and other sources.

## Pattern Categories

### Creational Patterns ✅ Complete (5/5)

Creational patterns deal with object creation mechanisms, trying to create objects in a manner suitable to the situation.

#### Factory Pattern
Creates objects without specifying the exact class to instantiate. Useful when the exact type of object is determined at runtime.

**Use When:**
- Object creation logic is complex
- You want to centralize object creation
- The exact type of object depends on configuration or user input

#### Singleton Pattern
Ensures a class has only one instance and provides a global point of access to it. Useful for managing shared resources like database connections or configuration.

**Use When:**
- Exactly one instance of a class is needed
- Controlled access to a single instance is necessary
- The instance should be extensible by subclassing

#### Builder Pattern
Separates the construction of a complex object from its representation. Useful when objects require many configuration parameters.

**Use When:**
- Object construction requires many parameters
- Objects need to be immutable after construction
- Construction process must allow different representations

#### Prototype Pattern
Creates new objects by cloning existing instances. Useful when object creation is expensive or complex.

**Use When:**
- Object creation is costly
- System should be independent of how objects are created
- Classes to instantiate are specified at runtime

#### Abstract Factory Pattern
Provides an interface for creating families of related or dependent objects without specifying their concrete classes.

**Use When:**
- System should be independent of how its objects are created
- System needs to work with multiple families of related objects
- You want to provide a library of objects without exposing implementation

### Behavioral Patterns ✅ Complete (11/11)

Behavioral patterns are concerned with algorithms and the assignment of responsibilities between objects.

#### Strategy Pattern
Defines a family of algorithms, encapsulates each one, and makes them interchangeable. Allows the algorithm to vary independently from clients that use it.

**Use When:**
- Many related classes differ only in their behavior
- You need different variants of an algorithm
- Algorithm uses data that clients shouldn't know about

#### Observer Pattern
Defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified automatically.

**Use When:**
- Changes to one object require changing others
- Number of dependent objects is unknown or dynamic
- An object should notify others without assumptions about who they are

#### Command Pattern
Encapsulates a request as an object, thereby allowing parameterization of clients with different requests, queue or log requests, and support undoable operations.

**Use When:**
- You want to parameterize objects by an action
- You need to queue, schedule, or execute requests at different times
- You need to support undo operations

#### Chain of Responsibility Pattern
Passes requests along a chain of handlers. Each handler decides either to process the request or pass it to the next handler in the chain.

**Use When:**
- More than one object may handle a request
- The handler is not known a priori
- The set of handlers should be specified dynamically

#### Interpreter Pattern
Defines a representation for a language's grammar along with an interpreter that uses the representation to interpret sentences in the language.

**Use When:**
- The grammar is simple
- Efficiency is not a critical concern
- The grammar changes frequently

#### State Pattern
Allows an object to alter its behavior when its internal state changes. The object will appear to change its class.

**Use When:**
- Object behavior depends on its state
- Operations have large conditional statements that depend on object state
- State transitions are explicit and numerous

#### Template Method Pattern
Defines the skeleton of an algorithm in a base class, allowing subclasses to override specific steps without changing the algorithm's structure.

**Use When:**
- You want to implement the invariant parts of an algorithm once
- Common behavior among subclasses should be localized
- You want to control subclass extensions at specific points

#### Iterator Pattern
Provides a way to access elements sequentially without exposing underlying representation. Python has built-in support for this pattern.

**Use When:**
- You need to traverse a collection without exposing its structure
- Multiple simultaneous traversals are needed
- You want a uniform interface for different collections

#### Visitor Pattern
Represents an operation to be performed on elements of an object structure. Lets you define new operations without changing the classes.

**Use When:**
- Object structure is stable but operations change frequently
- Many unrelated operations need to be performed on objects
- You want to separate algorithms from the objects they operate on

#### Mediator Pattern
Defines an object that encapsulates how a set of objects interact. Promotes loose coupling by preventing objects from referring to each other explicitly.

**Use When:**
- Objects communicate in complex ways with many dependencies
- Reusing objects is difficult due to tight coupling
- Behavior distributed among classes should be customizable

#### Memento Pattern
Captures and externalizes an object's internal state for later restoration without violating encapsulation.

**Use When:**
- Undo/redo functionality is needed
- Snapshots of state are required
- Direct access to state fields would violate encapsulation

### Structural Patterns ✅ Complete (7/7)

Structural patterns are concerned with how classes and objects are composed to form larger structures.

#### Decorator Pattern
Attaches additional responsibilities to an object dynamically. Provides a flexible alternative to subclassing for extending functionality.

**Use When:**
- Responsibilities need to be added to individual objects dynamically
- Extension by subclassing is impractical
- You want to add functionality without affecting other objects

#### Adapter Pattern
Converts the interface of a class into another interface clients expect. Allows classes to work together that couldn't otherwise due to incompatible interfaces.

**Use When:**
- You want to use an existing class with an incompatible interface
- You need to create a reusable class that cooperates with unrelated classes
- You need to use several existing subclasses but it's impractical to adapt their interface by subclassing

#### Composite Pattern
Composes objects into tree structures to represent part-whole hierarchies. Allows clients to treat individual objects and compositions uniformly.

**Use When:**
- You want to represent part-whole hierarchies
- You want clients to ignore the difference between compositions and individual objects
- The structure can be represented as a tree

#### Facade Pattern
Provides a simplified interface to a complex subsystem. Wraps complicated classes with a single, easier-to-use interface.

**Use When:**
- You want to provide a simple interface to a complex subsystem
- There are many dependencies between clients and implementation classes
- You want to layer your subsystems

#### Proxy Pattern
Provides a surrogate or placeholder for another object to control access to it. Useful for lazy loading, access control, or caching.

**Use When:**
- You need lazy initialization (virtual proxy)
- You need access control (protection proxy)
- You need to cache expensive operations (caching proxy)
- You need a local representative for a remote object (remote proxy)

#### Bridge Pattern
Decouples an abstraction from its implementation so that the two can vary independently. Uses composition to separate interface from implementation.

**Use When:**
- You want to avoid permanent binding between abstraction and implementation
- Both abstractions and implementations should be extensible by subclassing
- Changes in implementation should not impact clients

## Principles Demonstrated

### Composition over Inheritance
Demonstrates how composition provides more flexibility than inheritance by allowing behavior to be changed at runtime.

### Inheritance
Shows proper use of inheritance to model "is-a" relationships and share common behavior.

## Documentation Guides

This library includes comprehensive guides to help you master design patterns:

- **[Pattern Selection Guide](pattern_guide.md)** - Detailed guidance on when to use each pattern, including benefits, drawbacks, and trade-offs
- **[Pattern Comparison Guide](pattern_comparison.md)** - Side-by-side comparisons of similar patterns to help you choose the right one
- **[Practical Examples](practical_examples.md)** - Real-world use cases showing how patterns solve actual problems in web applications, microservices, and data processing
- **[Anti-Patterns](anti_patterns.md)** - Common mistakes and misuses to avoid when implementing patterns
- **[Quick Reference](quick_reference.md)** - Concise cheat sheet for rapid pattern selection and implementation

## Testing

All patterns include comprehensive test suites demonstrating correct usage and behavior. Run tests with:

```bash
pytest tests/
```

Current test statistics:
- 275+ tests
- 94% code coverage
- All 23 GoF patterns tested

## Type Checking

The codebase uses type hints throughout. Run type checking with:

```bash
mypy src/
```

## Best Practices

- All implementations follow Python idioms and conventions
- Type hints are used throughout for better IDE support and documentation
- Comprehensive docstrings explain the purpose and usage of each pattern
- Test coverage ensures correctness and demonstrates usage

## Contributing

When adding new patterns:
1. Create the pattern implementation in the appropriate category directory
2. Include comprehensive docstrings with examples
3. Add complete test coverage
4. Update this documentation

## References

- Design Patterns: Elements of Reusable Object-Oriented Software (Gang of Four)
- Head First Design Patterns
- Python-specific design patterns and idioms

## API Reference

::: design_patterns
    options:
      show_root_heading: true
      show_source: false
