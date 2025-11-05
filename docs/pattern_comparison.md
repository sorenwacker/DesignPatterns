# Pattern Comparison Guide

This guide helps you choose between similar patterns by comparing their purposes, use cases, and differences.

## Creational Pattern Comparisons

### Factory vs Abstract Factory vs Builder

| Aspect | Factory | Abstract Factory | Builder |
|--------|---------|------------------|---------|
| **Purpose** | Create single objects | Create families of objects | Construct complex objects |
| **Complexity** | Simple | Medium | High |
| **When to Use** | Single product type varies | Related products must work together | Many construction parameters |
| **Example** | Create different loggers | Create UI themes (button+checkbox+input) | Build computer with many specs |

**Choose Factory when:**
- You need to create one type of object
- Type determined at runtime
- Simple creation logic

**Choose Abstract Factory when:**
- Multiple related products must be created together
- Products come in families (Windows UI, Mac UI)
- System should be independent of product creation

**Choose Builder when:**
- Object has many optional parameters
- Construction requires multiple steps
- You want immutability with flexible construction

```python
# Factory: Create one thing
logger = LoggerFactory.create("file")

# Abstract Factory: Create family of related things
factory = WindowsFactory()
button = factory.create_button()
checkbox = factory.create_checkbox()

# Builder: Construct complex object step-by-step
computer = ComputerBuilder()
    .set_cpu("Intel i9")
    .set_ram(32)
    .set_storage("1TB")
    .build()
```

---

### Singleton vs Dependency Injection

| Aspect | Singleton | Dependency Injection |
|--------|-----------|---------------------|
| **Coupling** | Tight (global state) | Loose |
| **Testing** | Difficult | Easy |
| **Control** | Pattern controls creation | Framework controls |
| **Flexibility** | Limited | High |

**Prefer Dependency Injection when:**
- Testing is important
- Multiple instances might be needed in tests
- You want loose coupling

**Use Singleton only when:**
- Truly need one instance system-wide
- Testing complexity is acceptable
- Global access is genuinely needed

```python
# Singleton: Global state (harder to test)
config = Configuration()  # Always same instance

# Dependency Injection: Explicit dependencies (easier to test)
class UserService:
    def __init__(self, config: Configuration):
        self.config = config

# Testing with DI is easier
def test_user_service():
    test_config = Configuration()
    service = UserService(test_config)  # Use test config
```

---

## Behavioral Pattern Comparisons

### Strategy vs State vs Command

| Aspect | Strategy | State | Command |
|--------|----------|-------|---------|
| **Purpose** | Interchangeable algorithms | Behavior depends on state | Encapsulate requests |
| **Changes** | Algorithm | State | Operation |
| **Transitions** | No transitions | Has state transitions | No state |
| **Undo** | No | No | Yes |

**Choose Strategy when:**
- Multiple algorithms for same task
- Selection happens at runtime
- Algorithms are independent

**Choose State when:**
- Object behavior depends on its state
- Many state transitions
- State-specific behavior is complex

**Choose Command when:**
- You need undo/redo
- Operations should be queued/logged
- Parameterize objects with operations

```python
# Strategy: Pick algorithm at runtime
sorter = DataSorter(QuickSort())
sorter.sort(data)
sorter.set_strategy(MergeSort())

# State: Behavior changes with state
document.publish()  # Draft -> Moderation
document.approve()  # Moderation -> Published

# Command: Encapsulate operations for undo
cmd = SaveCommand(document)
cmd.execute()
cmd.undo()  # Restore previous state
```

---

### Observer vs Mediator vs Event Bus

| Aspect | Observer | Mediator | Event Bus |
|--------|----------|----------|-----------|
| **Communication** | One-to-many | Many-to-many through mediator | Publish/Subscribe |
| **Coupling** | Subject knows observers | Objects know mediator | Complete decoupling |
| **Complexity** | Simple | Medium | Low |

**Choose Observer when:**
- One object changes affect many others
- Relationships are one-directional
- Observers are independent

**Choose Mediator when:**
- Complex communication patterns
- Many objects interact
- Want to centralize control logic

**Choose Event Bus when:**
- Complete decoupling needed
- Publishers don't know subscribers
- Dynamic subscription needed

```python
# Observer: Subject notifies observers
weather_station.attach(phone_display)
weather_station.attach(tv_display)
weather_station.set_temperature(25)  # Both displays update

# Mediator: Central coordinator
chatroom = ChatRoom()
alice = User("Alice", chatroom)
bob = User("Bob", chatroom)
alice.send("Hi")  # Goes through chatroom

# Event Bus: Publish/Subscribe
bus.subscribe("user_registered", send_email)
bus.publish("user_registered", user_data)
```

---

### Template Method vs Strategy

| Aspect | Template Method | Strategy |
|--------|----------------|----------|
| **Mechanism** | Inheritance | Composition |
| **Flexibility** | Compile-time | Runtime |
| **Coupling** | Tighter | Looser |
| **Change** | Override methods | Swap objects |

**Choose Template Method when:**
- Algorithm structure is fixed
- Subclasses customize specific steps
- Inheritance is appropriate

**Choose Strategy when:**
- Algorithm can change at runtime
- Want to avoid inheritance
- Need algorithm objects to be reusable

```python
# Template Method: Override specific steps
class PDFParser(DocumentParser):
    def parse_header(self):  # Customize step
        return parse_pdf_header()

# Strategy: Swap entire algorithm
parser = DocumentParser()
parser.set_strategy(PDFParsingStrategy())  # Change at runtime
```

---

### Visitor vs Iterator

| Aspect | Visitor | Iterator |
|--------|---------|----------|
| **Purpose** | Add operations to structure | Traverse structure |
| **Structure** | Can be heterogeneous | Usually homogeneous |
| **Operations** | Many different operations | One operation (traversal) |

**Choose Visitor when:**
- Many unrelated operations on objects
- Object structure stable, operations change
- Operations need different algorithms

**Choose Iterator when:**
- Need to traverse collection
- Hide internal structure
- Support multiple traversals

```python
# Visitor: Different operations on same structure
shapes.accept(AreaCalculator())
shapes.accept(XMLExporter())
shapes.accept(PerimeterCalculator())

# Iterator: Traverse collection
for shape in shapes:  # Just iterate
    process(shape)
```

---

## Structural Pattern Comparisons

### Adapter vs Facade vs Proxy

| Aspect | Adapter | Facade | Proxy |
|--------|---------|--------|-------|
| **Purpose** | Interface compatibility | Simplify interface | Control access |
| **Relationship** | Converts interface | Simplifies complex system | Same interface |
| **When** | After design | Complex subsystem | Need control layer |

**Choose Adapter when:**
- Existing class has wrong interface
- Want to use incompatible interfaces
- Third-party integration needed

**Choose Facade when:**
- Complex subsystem needs simple interface
- Many dependencies exist
- Want to layer subsystems

**Choose Proxy when:**
- Need lazy initialization
- Access control required
- Want caching or logging

```python
# Adapter: Make incompatible interfaces work
adapter = LoggerAdapter(legacy_logger)
adapter.log_info("message")  # Adapts to new interface

# Facade: Simplify complex system
theater = HomeTheaterFacade()
theater.watch_movie("Inception")  # Hides complexity

# Proxy: Control access to object
image = ImageProxy("large_image.jpg")
image.display()  # Lazy loads only when needed
```

---

### Decorator vs Proxy vs Adapter

| Aspect | Decorator | Proxy | Adapter |
|--------|-----------|-------|---------|
| **Purpose** | Add behavior | Control access | Change interface |
| **Interface** | Same | Same | Different |
| **Stacking** | Yes | No | No |
| **Focus** | Enhancement | Control | Compatibility |

**Choose Decorator when:**
- Add responsibilities dynamically
- Stack multiple behaviors
- Want flexible enhancement

**Choose Proxy when:**
- Control object access
- Lazy loading needed
- Add indirection layer

**Choose Adapter when:**
- Interfaces don't match
- Want to reuse existing classes
- Third-party integration

```python
# Decorator: Stack behaviors
coffee = SimpleCoffee()
coffee = MilkDecorator(coffee)
coffee = SugarDecorator(coffee)  # Stack multiple

# Proxy: Control access
image = ImageProxy("image.jpg")  # Controls loading
if condition:
    image.display()  # Only loads if displayed

# Adapter: Convert interface
adapter = LoggerAdapter(old_logger)  # Changes interface
adapter.log_info("msg")  # New interface
```

---

### Composite vs Decorator

| Aspect | Composite | Decorator |
|--------|-----------|-----------|
| **Purpose** | Part-whole hierarchy | Add responsibilities |
| **Structure** | Tree | Linear |
| **Focus** | Structure | Behavior |
| **Uniformity** | Treat parts/wholes same | Enhance objects |

**Choose Composite when:**
- Represent part-whole hierarchies
- Want uniform treatment
- Tree structure fits domain

**Choose Decorator when:**
- Add behavior dynamically
- Want to stack features
- Avoid subclass explosion

```python
# Composite: Tree structure
group = CompositeShape()
group.add(Circle())
group.add(Rectangle())
group.draw()  # Draws all children

# Decorator: Linear wrapping
coffee = SimpleCoffee()
coffee = MilkDecorator(coffee)  # Wraps, not composes
```

---

### Bridge vs Strategy

| Aspect | Bridge | Strategy |
|--------|--------|----------|
| **Purpose** | Separate abstraction from implementation | Separate algorithms |
| **Scope** | Class level | Object level |
| **Variability** | Both abstraction and implementation | Algorithm only |

**Choose Bridge when:**
- Both abstraction and implementation vary
- Want to avoid class explosion
- Compile-time separation needed

**Choose Strategy when:**
- Only algorithm varies
- Runtime selection needed
- Simpler relationship

```python
# Bridge: Abstraction and implementation vary independently
circle = Circle(VectorRenderer())  # Abstraction + Implementation
square = Square(RasterRenderer())

# Strategy: Just algorithm varies
sorter = Sorter(QuickSort())  # Just algorithm changes
```

---

## Common Confusions

### When NOT to use patterns:

1. **Don't use Factory** if you only have one concrete class
2. **Don't use Singleton** if you're just avoiding passing parameters
3. **Don't use Abstract Factory** if products aren't related
4. **Don't use Builder** for simple objects
5. **Don't use Observer** for simple one-to-one relationships
6. **Don't use Mediator** if direct communication is simpler
7. **Don't use Visitor** if structure changes frequently
8. **Don't use Strategy** if you only have one algorithm
9. **Don't use State** for simple boolean flags
10. **Don't use Proxy** if direct access is sufficient

### Pattern Combinations:

**Common combinations that work well together:**

1. **Factory + Singleton**: Singleton factory for object creation
2. **Observer + Mediator**: Mediator coordinates observers
3. **Strategy + Factory**: Factory creates strategies
4. **Composite + Visitor**: Visit composite structures
5. **Decorator + Strategy**: Decorate strategy objects
6. **Builder + Prototype**: Builder creates prototype templates
7. **Command + Memento**: Commands store mementos for undo
8. **Proxy + Decorator**: Proxy with added behavior
9. **Facade + Singleton**: Singleton facade for subsystem
10. **Iterator + Composite**: Iterate composite structures

### Decision Tree:

```
Need to create objects?
├─ Single object → Factory
├─ Families of objects → Abstract Factory
├─ Complex construction → Builder
├─ Clone expensive objects → Prototype
└─ One instance → Singleton

Need to control behavior?
├─ Multiple algorithms → Strategy
├─ State-dependent behavior → State
├─ Encapsulate requests → Command
├─ Chain handling → Chain of Responsibility
└─ Traverse collection → Iterator

Need to control structure?
├─ Add behavior dynamically → Decorator
├─ Interface compatibility → Adapter
├─ Simplify complex system → Facade
├─ Control access → Proxy
├─ Part-whole hierarchy → Composite
└─ Separate abstraction/implementation → Bridge

Need object communication?
├─ One-to-many updates → Observer
├─ Centralize interaction → Mediator
└─ Add operations → Visitor

Need to manage state?
├─ Undo/redo → Memento
└─ Algorithm skeleton → Template Method
```
