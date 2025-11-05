# Design Patterns Quick Reference

A concise cheat sheet for choosing and implementing design patterns.

## Pattern Selection by Problem Type

### I need to create objects...

| Problem | Pattern | Quick Hint |
|---------|---------|------------|
| Type determined at runtime | **Factory** | `LoggerFactory.create("file")` |
| Need exactly one instance | **Singleton** | `Configuration()` always returns same |
| Many optional parameters | **Builder** | `Computer().set_cpu().set_ram().build()` |
| Expensive creation | **Prototype** | `clone()` instead of creating |
| Families of related objects | **Abstract Factory** | `factory.create_button()` + `factory.create_checkbox()` |

### I need to manage behavior...

| Problem | Pattern | Quick Hint |
|---------|---------|------------|
| Swap algorithms at runtime | **Strategy** | `sorter.set_strategy(QuickSort())` |
| Behavior depends on state | **State** | `order.state.ship()` changes state |
| Undo/redo functionality | **Command** | `cmd.execute()` then `cmd.undo()` |
| Undo/redo for complex state | **Memento** | Save/restore full snapshots |
| Pass request down chain | **Chain of Responsibility** | Request handled by first capable handler |
| One-to-many notifications | **Observer** | Subject notifies all observers |
| Complex object interactions | **Mediator** | Objects talk through mediator |
| Traverse collection | **Iterator** | `for item in collection` |
| Add operations to structure | **Visitor** | `structure.accept(visitor)` |
| Algorithm skeleton with steps | **Template Method** | Override specific steps |
| Parse simple grammar | **Interpreter** | Build syntax tree |

### I need to manage structure...

| Problem | Pattern | Quick Hint |
|---------|---------|------------|
| Add behavior dynamically | **Decorator** | Wrap object with new behavior |
| Incompatible interfaces | **Adapter** | Convert interface A to B |
| Simplify complex system | **Facade** | Single entry point |
| Control access | **Proxy** | Lazy load, cache, or protect |
| Part-whole hierarchy | **Composite** | Tree structure, uniform treatment |
| Separate abstraction/implementation | **Bridge** | Both vary independently |

---

## Pattern Categories at a Glance

### Creational (Object Creation)

```python
# Factory
logger = LoggerFactory.create("file")

# Singleton
config = Configuration()  # Always same instance

# Builder
computer = (ComputerBuilder()
    .set_cpu("i9")
    .set_ram(32)
    .build())

# Prototype
new_doc = existing_doc.clone()

# Abstract Factory
factory = WindowsFactory()
button = factory.create_button()
checkbox = factory.create_checkbox()
```

### Behavioral (Algorithms and Responsibilities)

```python
# Strategy
sorter.set_strategy(QuickSort())

# Observer
subject.attach(observer)
subject.notify()

# Command
cmd = SaveCommand(doc)
cmd.execute()
cmd.undo()

# State
order.state.ship()  # Changes to ShippedState

# Chain of Responsibility
handler1.set_next(handler2).set_next(handler3)

# Iterator
for item in collection:
    process(item)

# Visitor
shape.accept(AreaCalculator())

# Mediator
chatroom.send_message(user, "Hello")

# Memento
snapshot = editor.save()
editor.restore(snapshot)

# Template Method
class PDFParser(DocumentParser):
    def parse_header(self):
        return parse_pdf_header()

# Interpreter
expression = "2 + 3 * 4"
result = interpreter.evaluate(expression)
```

### Structural (Object Composition)

```python
# Decorator
coffee = MilkDecorator(SugarDecorator(SimpleCoffee()))

# Adapter
adapter = ModernAdapter(legacy_system)

# Facade
facade.complex_operation()  # Hides many subsystems

# Proxy
proxy = ImageProxy("large.jpg")  # Loads on demand

# Composite
group = CompositeShape()
group.add(Circle())
group.add(Rectangle())
group.draw()  # Draws all

# Bridge
shape = Circle(VectorRenderer())
```

---

## Common Pattern Combinations

| Scenario | Combination | Example |
|----------|-------------|---------|
| Creating strategies | Factory + Strategy | `strategy = StrategyFactory.create("quick_sort")` |
| Coordinating observers | Mediator + Observer | Mediator manages observers |
| Single factory instance | Singleton + Factory | One factory instance |
| Undoable commands | Command + Memento | Commands save mementos |
| Iterating composites | Composite + Iterator | Traverse tree structure |
| Visiting composites | Composite + Visitor | Operations on tree |
| Proxy with features | Proxy + Decorator | Proxy with added behavior |
| Facade as singleton | Facade + Singleton | One subsystem interface |

---

## Decision Trees

### Creating Objects?

```
Do you need to...
├─ Create different types at runtime?
│  └─ Use FACTORY
├─ Have exactly one instance?
│  └─ Use SINGLETON
├─ Construct with many parameters?
│  └─ Use BUILDER
├─ Clone expensive objects?
│  └─ Use PROTOTYPE
└─ Create families of related objects?
   └─ Use ABSTRACT FACTORY
```

### Managing Behavior?

```
Do you need to...
├─ Swap algorithms?
│  └─ Use STRATEGY
├─ Change behavior based on state?
│  └─ Use STATE
├─ Support undo/redo?
│  ├─ Simple operations? → Use COMMAND
│  └─ Complex state? → Use MEMENTO
├─ Pass requests down a chain?
│  └─ Use CHAIN OF RESPONSIBILITY
├─ Notify multiple objects?
│  └─ Use OBSERVER
├─ Centralize complex interactions?
│  └─ Use MEDIATOR
├─ Traverse a collection?
│  └─ Use ITERATOR
├─ Add operations to structure?
│  └─ Use VISITOR
├─ Define algorithm skeleton?
│  └─ Use TEMPLATE METHOD
└─ Parse expressions?
   └─ Use INTERPRETER
```

### Managing Structure?

```
Do you need to...
├─ Add responsibilities dynamically?
│  └─ Use DECORATOR
├─ Convert an interface?
│  └─ Use ADAPTER
├─ Simplify complex subsystem?
│  └─ Use FACADE
├─ Control access to object?
│  └─ Use PROXY
├─ Represent part-whole hierarchy?
│  └─ Use COMPOSITE
└─ Vary abstraction and implementation independently?
   └─ Use BRIDGE
```

---

## Python-Specific Considerations

### Built-in Pattern Support

| Pattern | Python Feature | Example |
|---------|----------------|---------|
| Iterator | `__iter__`, `__next__` | `for x in obj` |
| Decorator | `@decorator` syntax | `@cache`, `@property` |
| Context Manager | `__enter__`, `__exit__` | `with open("file") as f` |
| Singleton | Module-level variable | Import module once |
| Observer | `property` descriptors | Automatic notifications |
| Strategy | First-class functions | Pass function as parameter |

### When NOT to Use Patterns in Python

```python
# ❌ Don't create Iterator class for simple iteration
# ✅ Use generator
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# ❌ Don't create Singleton class for configuration
# ✅ Use module-level variables
# config.py
DATABASE_URL = "postgresql://..."
DEBUG = True

# ❌ Don't create Strategy classes for simple functions
# ✅ Use first-class functions
def process(data, transform_func):
    return transform_func(data)

process(data, lambda x: x * 2)
process(data, str.upper)
```

---

## Pattern Complexity Scale

### Low Complexity (Start Here)
- **Factory** - Simple object creation
- **Strategy** - Swap algorithms
- **Decorator** - Add features
- **Adapter** - Interface conversion
- **Iterator** - Traverse collections

### Medium Complexity
- **Observer** - Event notifications
- **Command** - Encapsulate actions
- **Template Method** - Algorithm skeleton
- **Facade** - Simplify subsystem
- **Proxy** - Control access
- **Composite** - Tree structures
- **Builder** - Complex construction

### High Complexity (Use When Justified)
- **State** - Complex state transitions
- **Mediator** - Many interactions
- **Visitor** - Operations on structures
- **Chain of Responsibility** - Dynamic handling
- **Abstract Factory** - Product families
- **Bridge** - Dual hierarchies
- **Interpreter** - Language parsing
- **Memento** - State snapshots
- **Prototype** - Complex cloning

---

## Quick Implementation Templates

### Factory Pattern

```python
class AnimalFactory:
    @staticmethod
    def create(animal_type: str, name: str):
        if animal_type == "dog":
            return Dog(name)
        elif animal_type == "cat":
            return Cat(name)
        raise ValueError(f"Unknown type: {animal_type}")
```

### Singleton Pattern

```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### Builder Pattern

```python
class Builder:
    def __init__(self):
        self._product = Product()

    def set_feature(self, value):
        self._product.feature = value
        return self

    def build(self):
        return self._product
```

### Strategy Pattern

```python
class Context:
    def __init__(self, strategy):
        self._strategy = strategy

    def execute(self, data):
        return self._strategy.execute(data)
```

### Observer Pattern

```python
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)
```

### Decorator Pattern

```python
class Decorator:
    def __init__(self, component):
        self._component = component

    def operation(self):
        return self._component.operation() + " + extra"
```

### Adapter Pattern

```python
class Adapter:
    def __init__(self, adaptee):
        self._adaptee = adaptee

    def request(self):
        return self._adaptee.specific_request()
```

---

## Red Flags (When NOT to Use Patterns)

| Red Flag | What It Means |
|----------|---------------|
| Only one implementation | Don't use Factory/Abstract Factory |
| Simple boolean state | Don't use State pattern |
| 2-3 parameters | Don't use Builder |
| Simple operations | Don't use Command |
| No undo/complex state | Don't use Memento |
| Direct communication works | Don't use Mediator |
| Structure changes often | Don't use Visitor |
| Single algorithm | Don't use Strategy |
| Simple access | Don't use Proxy |
| You control both interfaces | Don't use Adapter |

---

## Pattern Selection Checklist

Before applying any pattern, ask:

1. **What problem am I solving?**
   - Be specific about the actual problem

2. **Is the problem recurring?**
   - Patterns solve recurring problems

3. **What's the simplest solution?**
   - Try simple first, refactor to pattern if needed

4. **Does the pattern make it simpler?**
   - If not, don't use it

5. **Will others understand it?**
   - Code should be clear to team members

6. **Does it make testing easier?**
   - Good patterns improve testability

7. **Is it a Python idiom?**
   - Prefer Python's built-in features when available

---

## Learning Path

### Beginner - Start Here
1. **Factory** - Basic object creation
2. **Strategy** - Swap behavior
3. **Decorator** - Add features
4. **Adapter** - Interface conversion

### Intermediate - Common in Practice
5. **Singleton** - One instance
6. **Observer** - Events
7. **Command** - Actions as objects
8. **Facade** - Simplify complexity
9. **Template Method** - Algorithm skeleton
10. **Iterator** - Traversal

### Advanced - Specific Use Cases
11. **Builder** - Complex construction
12. **State** - State machines
13. **Composite** - Tree structures
14. **Proxy** - Access control
15. **Abstract Factory** - Product families
16. **Chain of Responsibility** - Handler chains
17. **Mediator** - Complex interactions
18. **Visitor** - Operations on structures
19. **Memento** - State snapshots
20. **Bridge** - Dual variation
21. **Prototype** - Cloning
22. **Interpreter** - Language parsing

---

## Quick Reference: Pattern vs Problem

| I need to... | Use This Pattern |
|-------------|------------------|
| Create objects without specifying exact class | Factory |
| Ensure only one instance exists | Singleton |
| Build object with many parameters | Builder |
| Clone expensive objects | Prototype |
| Create families of related objects | Abstract Factory |
| Swap algorithms at runtime | Strategy |
| Notify multiple objects of changes | Observer |
| Support undo/redo operations | Command or Memento |
| Implement state machine | State |
| Pass request down chain of handlers | Chain of Responsibility |
| Add behavior without changing class | Decorator |
| Make incompatible interfaces work | Adapter |
| Simplify complex subsystem | Facade |
| Control access to object | Proxy |
| Represent part-whole hierarchy | Composite |
| Separate abstraction from implementation | Bridge |
| Traverse collection | Iterator |
| Add operations to object structure | Visitor |
| Centralize object communication | Mediator |
| Define algorithm skeleton | Template Method |
| Parse simple language | Interpreter |

---

## Summary: Think in Questions

1. **Creation**: How should objects be created?
   → Creational Patterns

2. **Behavior**: How should objects behave and collaborate?
   → Behavioral Patterns

3. **Structure**: How should objects be composed?
   → Structural Patterns

**Most Important Rule**: Use patterns to solve problems, not to demonstrate knowledge of patterns. Simple, clear code beats pattern-heavy code every time.
