# Pattern Catalog

## Creational Patterns

| Pattern | Purpose | Key Benefit |
|---------|---------|-------------|
| **Factory** | Create objects without specifying exact class | Encapsulates object creation logic |
| **Singleton** | Ensure only one instance exists | Controlled access to single instance |
| **Builder** | Construct complex objects step by step | Separates construction from representation |
| **Prototype** | Clone objects instead of creating new ones | Avoids expensive initialization |
| **Abstract Factory** | Create families of related objects | Ensures product compatibility |

## Behavioral Patterns

| Pattern | Purpose | Key Benefit |
|---------|---------|-------------|
| **Strategy** | Define interchangeable algorithm families | Runtime algorithm selection |
| **Observer** | Notify dependents of state changes | Loose coupling between objects |
| **Command** | Encapsulate requests as objects | Parameterize and queue operations |
| **Chain of Responsibility** | Pass requests along handler chain | Decouples sender from receiver |
| **Interpreter** | Interpret language grammar | Represents grammar rules as classes |
| **State** | Alter behavior when internal state changes | State-specific behavior encapsulation |
| **Template Method** | Define algorithm skeleton in base class | Subclasses override specific steps |
| **Iterator** | Access elements sequentially | Uniform traversal interface |
| **Visitor** | Separate algorithms from object structure | Add operations without modifying classes |
| **Mediator** | Reduce coupling between communicating objects | Centralized communication |
| **Memento** | Capture and restore object state | Externalized state management |

## Structural Patterns

| Pattern | Purpose | Key Benefit |
|---------|---------|-------------|
| **Decorator** | Add responsibilities dynamically | Flexible alternative to subclassing |
| **Adapter** | Make incompatible interfaces work together | Interface compatibility |
| **Composite** | Treat individual and composed objects uniformly | Tree structure representation |
| **Facade** | Provide simplified interface to complex subsystem | Reduces system complexity |
| **Proxy** | Control access to another object | Lazy initialization, access control |
| **Bridge** | Decouple abstraction from implementation | Independent variation of abstractions |

## Testing Patterns

| Pattern | Purpose | Key Benefit |
|---------|---------|-------------|
| **Fixture** | Provide fixed baseline state for tests | Reusable test setup and consistent test data |

## Gate Patterns

| Pattern | Purpose | Key Benefit |
|---------|---------|-------------|
| **Absence** | Assert a withdrawn name stays withdrawn | Carries the removal reason forward |
| **Population** | Assert only one implementation of a kind exists | Detects duplicates by shape, not by name |
| **Contract** | Assert a substitute matches the real collaborator | Catches signature and asynchrony drift |
| **Grandfathered Debt** | Apply a limit forward while tolerating existing violations | Ratchets debt downward without a retrofit |
| **Boundary** | Assert a layer does not know about another | Enforces layering, including vocabulary |
| **Live Contract** | Assert beliefs about an external system are true of it | Detects silent acceptance and discard |
| **Read-After-Write** | Confirm a write landed by reading it back | Separates a refused write from a discarded one |
