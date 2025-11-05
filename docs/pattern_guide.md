# Design Pattern Selection Guide

This guide helps you choose the right pattern for your situation by explaining when to use each pattern, when to avoid it, and the trade-offs involved.

## Creational Patterns

### Factory Pattern

**When to Use:**
- Object creation logic is complex or subject to change
- You need to centralize object creation
- The exact type depends on runtime configuration
- You want to hide implementation details from clients

**When NOT to Use:**
- Object creation is simple and unlikely to change
- You only have one concrete class
- Clients need direct access to concrete types

**Benefits:**
- Loose coupling between client and concrete classes
- Single Responsibility - creation logic in one place
- Open/Closed - easy to add new types without modifying existing code

**Drawbacks:**
- Can introduce unnecessary complexity for simple cases
- May require many factory classes for different product families

---

### Singleton Pattern

**When to Use:**
- Exactly one instance must exist (e.g., configuration, logging)
- Global access point is needed
- Lazy initialization is beneficial
- Resource sharing is required (database connections, thread pools)

**When NOT to Use:**
- Testing is difficult (global state makes unit testing hard)
- Multithreading requires careful synchronization
- Multiple instances might be needed in the future
- It's being used as a global variable (code smell)

**Benefits:**
- Controlled access to sole instance
- Lazy initialization saves resources
- Reduced namespace pollution

**Drawbacks:**
- Violates Single Responsibility Principle (controls creation + business logic)
- Difficult to unit test (global mutable state)
- Can hide dependencies
- Thread safety requires extra care

---

### Builder Pattern

**When to Use:**
- Object requires many parameters (especially optional ones)
- Object construction is complex with multiple steps
- You want immutable objects with flexible construction
- Validation logic is needed during construction

**When NOT to Use:**
- Objects are simple with few parameters
- Object construction is straightforward
- You don't need fluent interface or step-by-step construction

**Benefits:**
- Clear, readable construction code (fluent interface)
- Can construct different representations with same process
- Isolates complex construction code
- Supports immutability

**Drawbacks:**
- Increases code complexity
- Requires creating additional builder classes
- May be overkill for simple objects

---

### Prototype Pattern

**When to Use:**
- Object creation is expensive (database queries, network calls)
- System should be independent of how products are created
- Classes to instantiate are specified at runtime
- You need to avoid subclass explosion

**When NOT to Use:**
- Objects don't have complex initialization
- Deep copying is difficult (circular references, external resources)
- You need different initialization for each instance

**Benefits:**
- Reduces need for subclasses
- Avoids expensive initialization
- Can add/remove objects at runtime
- Configures objects with various values dynamically

**Drawbacks:**
- Cloning complex objects with circular references is difficult
- Each subclass must implement cloning
- Deep copy vs shallow copy can be tricky

---

### Abstract Factory Pattern

**When to Use:**
- System needs to be independent of how objects are created
- System should work with multiple families of related products
- Family of related objects must be used together
- You want to provide class library without exposing implementations

**When NOT to Use:**
- Product families don't need to be consistent
- Adding new product types is frequent (hard to extend)
- Only one family exists

**Benefits:**
- Isolates concrete classes
- Makes exchanging product families easy
- Promotes consistency among products
- Supports Open/Closed principle for families

**Drawbacks:**
- Difficult to support new kinds of products
- Increases complexity with multiple factory classes
- Can be overkill for simple cases

## Behavioral Patterns

### Strategy Pattern

**When to Use:**
- You have multiple algorithms for a specific task
- Algorithm selection happens at runtime
- You want to avoid conditional statements for algorithm selection
- Algorithms use data that clients shouldn't know about

**When NOT to Use:**
- You only have one algorithm
- Algorithms rarely change
- Overhead of additional objects is unjustified

**Benefits:**
- Eliminates conditional statements
- Easier to add new algorithms
- Can switch algorithms at runtime
- Cleaner, more maintainable code

**Drawbacks:**
- Clients must understand different strategies
- Increases number of objects
- Communication overhead between strategy and context

---

### Observer Pattern

**When to Use:**
- One object's state changes affect multiple others
- Number of dependents is unknown or dynamic
- You want loose coupling between subject and observers
- Broadcasting is needed

**When NOT to Use:**
- Observer relationships are simple and fixed
- Performance is critical (notification overhead)
- Order of notifications matters

**Benefits:**
- Loose coupling between subject and observers
- Dynamic relationships
- Broadcast communication
- Supports Open/Closed principle

**Drawbacks:**
- Unexpected updates (cascade of notifications)
- Memory leaks if observers aren't properly removed
- No guarantee on notification order
- Can be hard to debug

---

### Command Pattern

**When to Use:**
- You need to parameterize objects with operations
- You want to queue, schedule, or log operations
- Undo/redo functionality is needed
- Transactions are required

**When NOT to Use:**
- Operations are simple and don't need to be objects
- No need for undo, queuing, or logging
- Performance overhead isn't acceptable

**Benefits:**
- Decouples invoker from receiver
- Easy to add new commands
- Supports undo/redo
- Can assemble commands into composite commands

**Drawbacks:**
- Increases number of classes
- Can be overkill for simple operations
- May complicate simple designs

---

### Iterator Pattern

**When to Use:**
- You need to access elements without exposing internal structure
- Collection supports multiple traversal methods
- You want a uniform interface for different collections

**When NOT to Use:**
- Collection structure is simple (use built-in iteration)
- Only one traversal method is needed
- Python's built-in iterators are sufficient

**Benefits:**
- Supports multiple simultaneous traversals
- Simplifies collection interface
- More than one traversal algorithm possible
- Python's for-loops work automatically

**Drawbacks:**
- Can be overkill for simple collections
- Less efficient than direct traversal
- Python already provides excellent iteration support

---

### State Pattern

**When to Use:**
- Object behavior depends on its state
- Operations have large multi-part conditional statements
- State transitions are explicit
- You want to avoid flag/enum-based state management

**When NOT to Use:**
- Few states and simple transitions
- State logic is straightforward
- States are unlikely to change

**Benefits:**
- Localizes state-specific behavior
- Makes state transitions explicit
- Easier to add new states
- Eliminates complex conditionals

**Drawbacks:**
- Increases number of classes
- Can be overkill for simple state machines
- State transitions spread across classes

---

### Template Method Pattern

**When to Use:**
- Algorithm skeleton should be fixed but steps vary
- Common behavior should be in one place
- You want to control extension points
- Subclass behavior needs to be customized

**When NOT to Use:**
- Algorithm has no common structure
- Each subclass completely overrides behavior
- Inheritance is not appropriate

**Benefits:**
- Code reuse for common algorithm structure
- Inversion of Control
- Protected variations in algorithm
- Easy to add new variations

**Drawbacks:**
- Uses inheritance (tight coupling)
- Can make code harder to understand
- Violates Liskov Substitution if not careful
- Maintenance issues with deep inheritance

---

### Visitor Pattern

**When to Use:**
- You need to perform operations across unrelated classes
- Object structure is stable but operations change frequently
- Many unrelated operations need to be performed
- You want to separate algorithm from objects

**When NOT to Use:**
- Object structure changes frequently (every change breaks visitors)
- Operations are closely related to object structure
- Few operations are needed

**Benefits:**
- Easy to add new operations
- Related operations are grouped together
- Can accumulate state while visiting
- Separation of concerns

**Drawbacks:**
- Hard to add new element classes
- Breaks encapsulation
- Circular dependencies between visitors and elements
- Can be complex to understand

---

### Mediator Pattern

**When to Use:**
- Objects communicate in complex ways
- Reusing objects is difficult due to many dependencies
- Behavior distributed among classes needs to be customized
- Too many interconnections between objects

**When NOT to Use:**
- Communication patterns are simple
- Few objects need to communicate
- Direct communication is clearer

**Benefits:**
- Decouples colleagues
- Centralizes control
- Simplifies object protocols
- Easier to understand object cooperation

**Drawbacks:**
- Mediator can become complex "god object"
- Can be hard to maintain
- Single point of failure

---

### Memento Pattern

**When to Use:**
- Undo/redo functionality is needed
- Object state snapshots are required
- Direct access to state would violate encapsulation
- Checkpoints/rollback is needed

**When NOT to Use:**
- State is simple and can be reconstructed
- Memory overhead is prohibitive
- State changes are infrequent

**Benefits:**
- Preserves encapsulation
- Simplifies originator
- Easy to implement undo/redo
- Can save state at any time

**Drawbacks:**
- Can be expensive if state is large
- Memory intensive for many mementos
- Caretaker must track memento lifecycle
- Hidden costs in copying state

---

### Chain of Responsibility Pattern

**When to Use:**
- Multiple objects can handle a request
- Handler set should be dynamic
- You want to issue requests without knowing the receiver
- Order of handling matters

**When NOT to Use:**
- All requests must be handled (no guarantee in chain)
- Performance is critical
- Handler order is unclear

**Benefits:**
- Reduced coupling
- Flexibility in assigning responsibilities
- Easy to add/remove handlers
- Request handling can be dynamic

**Drawbacks:**
- No guarantee request will be handled
- Hard to observe runtime characteristics
- Can affect performance

---

### Interpreter Pattern

**When to Use:**
- Grammar is simple
- Grammar changes frequently
- Efficiency is not critical
- You're building a scripting language or expression evaluator

**When NOT to Use:**
- Grammar is complex (use parser generators)
- Performance is critical
- Grammar is stable (interpreter overhead not justified)

**Benefits:**
- Easy to change and extend grammar
- Easy to implement grammar
- Complex grammars maintainable

**Drawbacks:**
- Complex grammars are hard to maintain
- Inefficient for complex grammars
- Difficult to optimize

## Structural Patterns

### Decorator Pattern

**When to Use:**
- You need to add responsibilities dynamically
- Extension by subclassing is impractical
- You want to add features without affecting other objects
- Behaviors can be combined in various ways

**When NOT to Use:**
- Simple functionality doesn't need decoration
- Too many small classes result
- Order of decoration matters (can be confusing)

**Benefits:**
- More flexible than inheritance
- Responsibilities can be added/removed at runtime
- Pay-per-use approach (only decorated objects have overhead)
- Avoids feature-laden classes high in hierarchy

**Drawbacks:**
- Many small objects
- Hard to remove specific decorators from stack
- Identity of decorated object changes
- Order can matter

---

### Adapter Pattern

**When to Use:**
- You want to use an existing class with incompatible interface
- You need to create reusable class that cooperates with unrelated classes
- Multiple existing subclasses need interface adaptation
- Third-party libraries need interface translation

**When NOT to Use:**
- You control both interfaces (just change them)
- Simple forwarding is overkill
- Interfaces are similar enough

**Benefits:**
- Reuse existing code
- Clean separation of interface adaptation
- Single responsibility for adaptation
- Transparent to clients

**Drawbacks:**
- Increases overall complexity
- Sometimes simpler to just change the source
- Can introduce performance overhead

---

### Composite Pattern

**When to Use:**
- You want to represent part-whole hierarchies
- Clients should ignore differences between compositions and individuals
- Tree structures are needed
- Uniform treatment of objects is desired

**When NOT to Use:**
- Tree structure doesn't fit the domain
- Operations differ significantly between leaf and composite
- Clients need to treat leaf and composite differently

**Benefits:**
- Defines class hierarchies of primitive and complex objects
- Makes client simple
- Easy to add new component types
- Provides flexibility of structure

**Drawbacks:**
- Can make design overly general
- Hard to restrict components
- Can be difficult to enforce type constraints

---

### Facade Pattern

**When to Use:**
- You want simple interface to complex subsystem
- Many dependencies exist between clients and implementation
- You want to layer subsystems
- You're wrapping legacy code

**When NOT to Use:**
- Subsystem is already simple
- Clients need access to all subsystem features
- You're hiding necessary complexity

**Benefits:**
- Shields clients from subsystem components
- Promotes weak coupling
- Layering subsystems
- Hides complexity

**Drawbacks:**
- Can become a god object
- May limit access to advanced features
- Additional layer can reduce performance

---

### Proxy Pattern

**When to Use:**
- You need lazy initialization (virtual proxy)
- Access control is needed (protection proxy)
- Caching is beneficial (caching proxy)
- Remote object representation needed (remote proxy)

**When NOT to Use:**
- Direct access is simpler and sufficient
- Overhead isn't justified
- Simple operations don't need proxying

**Benefits:**
- Controls access to object
- Can add extra functionality transparently
- Lazy initialization saves resources
- Protection without changing object

**Drawbacks:**
- Adds complexity
- May introduce latency
- Can make code harder to understand

---

### Bridge Pattern

**When to Use:**
- You want to avoid permanent binding between abstraction and implementation
- Both abstractions and implementations should be extensible
- Changes in implementation shouldn't affect clients
- Implementation should be selected/switched at runtime

**When NOT to Use:**
- Single implementation exists
- Hierarchy is shallow
- Abstraction and implementation aren't likely to vary independently

**Benefits:**
- Decouples interface from implementation
- Improves extensibility
- Hides implementation from clients
- Can change implementation at runtime

**Drawbacks:**
- Increases complexity
- May be overkill for simple cases
- Requires careful design upfront

## Pattern Selection Tips

1. **Start Simple**: Don't use patterns "just because" - use them when they solve a real problem
2. **Refactor to Patterns**: Often better to refactor into patterns when complexity demands it
3. **Combine Patterns**: Many real systems use multiple patterns together
4. **Consider Python Idioms**: Python's features (duck typing, first-class functions) may eliminate need for some patterns
5. **Balance**: Patterns add structure but also complexity - find the right balance
