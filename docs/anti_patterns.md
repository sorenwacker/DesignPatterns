# Anti-Patterns and Common Mistakes

This guide covers common misuses and pitfalls when implementing design patterns. Learning what NOT to do is as important as learning what to do.

## Table of Contents

- [Creational Anti-Patterns](#creational-anti-patterns)
- [Behavioral Anti-Patterns](#behavioral-anti-patterns)
- [Structural Anti-Patterns](#structural-anti-patterns)
- [General Anti-Patterns](#general-anti-patterns)

## Creational Anti-Patterns

### Singleton Abuse

**The Problem:**
Using Singleton as a global variable container instead of for legitimate single-instance requirements.

**Bad Example:**
```python
# Anti-pattern: Singleton as global state dump
class GlobalState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.user_data = {}
            cls._instance.temp_values = []
            cls._instance.random_stuff = None
        return cls._instance

# Everything becomes global state
state = GlobalState()
state.user_data['current'] = user
state.temp_values.append(123)
```

**Why It's Bad:**
- Creates hidden dependencies
- Makes testing impossible (global mutable state)
- Violates Single Responsibility Principle
- Tight coupling across entire codebase

**Better Approach:**
```python
# Use dependency injection
class UserService:
    def __init__(self, config: Configuration):
        self.config = config

    def get_user(self, user_id: int):
        # Use injected config, not global state
        return database.query(User).get(user_id)

# Explicit dependencies
service = UserService(config=app_config)
```

**When Singleton IS Appropriate:**
- Logger (one logging system)
- Database connection pool (managed resource)
- Configuration loaded once from file
- Thread pool or cache

---

### Factory Method Overkill

**The Problem:**
Creating factory methods for simple object creation that doesn't need abstraction.

**Bad Example:**
```python
# Anti-pattern: Unnecessary factory
class UserFactory:
    @staticmethod
    def create_user(name: str, email: str) -> User:
        return User(name=name, email=email)

# Usage is more complex than direct creation
user = UserFactory.create_user("John", "john@example.com")

# When this would be clearer:
user = User(name="John", email="john@example.com")
```

**Why It's Bad:**
- Adds unnecessary indirection
- No benefit over direct instantiation
- Makes code harder to follow
- False sense of "using patterns"

**When Factory IS Appropriate:**
```python
# Good: Complex creation logic
class DatabaseConnectionFactory:
    @staticmethod
    def create_connection(db_type: str):
        if db_type == "postgres":
            conn = PostgreSQLConnection()
            conn.configure_ssl()
            conn.set_pool_size(10)
            return conn
        elif db_type == "mysql":
            conn = MySQLConnection()
            conn.enable_utf8mb4()
            return conn
        # Complex, varying logic justifies factory
```

---

### Builder for Simple Objects

**The Problem:**
Using Builder pattern for objects with few parameters or simple construction.

**Bad Example:**
```python
# Anti-pattern: Builder overkill
class UserBuilder:
    def __init__(self):
        self._name = None
        self._email = None

    def set_name(self, name):
        self._name = name
        return self

    def set_email(self, email):
        self._email = email
        return self

    def build(self):
        return User(self._name, self._email)

# More complex than necessary
user = UserBuilder().set_name("John").set_email("john@example.com").build()

# vs simple constructor
user = User(name="John", email="john@example.com")
```

**Why It's Bad:**
- Adds complexity without benefit
- More code to maintain
- No advantage over constructor

**When Builder IS Appropriate:**
```python
# Good: Many optional parameters
computer = (ComputerBuilder()
    .set_cpu("Intel i9")
    .set_ram(32)
    .set_storage("1TB SSD")
    .set_gpu("RTX 4090")
    .add_monitor("4K Dell")
    .add_monitor("4K Samsung")
    .set_keyboard("Mechanical")
    .set_mouse("Logitech")
    .enable_rgb_lighting()
    .build())
```

---

### Abstract Factory Premature Abstraction

**The Problem:**
Creating abstract factories before you have multiple families of products.

**Bad Example:**
```python
# Anti-pattern: Over-engineering
class ButtonFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

class WindowsButtonFactory(ButtonFactory):
    def create_button(self) -> Button:
        return WindowsButton()

# Only one implementation exists, no need for abstraction yet
```

**Why It's Bad:**
- YAGNI violation (You Aren't Gonna Need It)
- Added complexity for future flexibility that may never be needed
- Harder to understand and maintain

**When Abstract Factory IS Appropriate:**
```python
# Good: Multiple families exist
windows_factory = WindowsGUIFactory()  # Windows themed UI
mac_factory = MacOSGUIFactory()        # macOS themed UI
linux_factory = LinuxGUIFactory()      # Linux themed UI

# Each creates consistent family
button = factory.create_button()
checkbox = factory.create_checkbox()
input_field = factory.create_input()
```

---

## Behavioral Anti-Patterns

### Strategy for Single Algorithm

**The Problem:**
Using Strategy pattern when only one algorithm exists or will ever exist.

**Bad Example:**
```python
# Anti-pattern: Unnecessary strategy
class AdditionStrategy:
    def execute(self, a, b):
        return a + b

class Calculator:
    def __init__(self):
        self.strategy = AdditionStrategy()

    def calculate(self, a, b):
        return self.strategy.execute(a, b)

# Just do: result = a + b
```

**Why It's Bad:**
- Over-engineering simple operations
- No flexibility gained
- More objects to manage

**When Strategy IS Appropriate:**
```python
# Good: Multiple algorithms
sorter = DataSorter(QuickSort())
sorter.sort(small_data)

sorter.set_strategy(MergeSort())
sorter.sort(large_data)

sorter.set_strategy(BubbleSort())
sorter.sort(nearly_sorted_data)
```

---

### Observer Memory Leaks

**The Problem:**
Forgetting to unsubscribe observers, causing memory leaks.

**Bad Example:**
```python
# Anti-pattern: No cleanup
class UserInterface:
    def __init__(self, data_source):
        self.data_source = data_source
        data_source.attach(self)  # Attaches but never detaches

    def update(self, data):
        self.render(data)

# Problem: UI objects never get garbage collected
for i in range(1000):
    ui = UserInterface(data_source)  # Each attached, none removed
    # ui goes out of scope but still referenced by data_source
```

**Why It's Bad:**
- Memory leaks
- Observers receive updates after they should be destroyed
- Performance degradation over time

**Better Approach:**
```python
# Good: Proper cleanup
class UserInterface:
    def __init__(self, data_source):
        self.data_source = data_source
        data_source.attach(self)

    def close(self):
        self.data_source.detach(self)  # Cleanup

    def __del__(self):
        if self.data_source:
            self.data_source.detach(self)

# Or use weak references
import weakref

class Subject:
    def __init__(self):
        self._observers = weakref.WeakSet()  # Auto cleanup
```

---

### Command Pattern for Everything

**The Problem:**
Wrapping every action in a command object when simpler approaches work.

**Bad Example:**
```python
# Anti-pattern: Command overkill for simple operations
class PrintCommand:
    def __init__(self, text):
        self.text = text

    def execute(self):
        print(self.text)

cmd = PrintCommand("Hello")
cmd.execute()

# Just do: print("Hello")
```

**Why It's Bad:**
- Unnecessary complexity
- No undo/redo needed
- No queuing needed
- More code without benefit

**When Command IS Appropriate:**
```python
# Good: Need undo/redo
class TextEditor:
    def __init__(self):
        self.content = ""
        self.history = []

    def execute_command(self, cmd):
        cmd.execute()
        self.history.append(cmd)

    def undo(self):
        if self.history:
            cmd = self.history.pop()
            cmd.undo()

# Commands support undo
editor.execute_command(InsertTextCommand(editor, "Hello"))
editor.execute_command(DeleteTextCommand(editor, 0, 5))
editor.undo()  # Restore deleted text
```

---

### State Machine for Boolean Flags

**The Problem:**
Using State pattern for simple true/false states.

**Bad Example:**
```python
# Anti-pattern: Over-engineered boolean
class OnState:
    def toggle(self, light):
        light.state = OffState()

class OffState:
    def toggle(self, light):
        light.state = OnState()

class Light:
    def __init__(self):
        self.state = OffState()

    def toggle(self):
        self.state.toggle(self)

# Just use: self.is_on = not self.is_on
```

**Why It's Bad:**
- Too many classes for simple logic
- Over-complicates boolean state
- Harder to understand

**When State IS Appropriate:**
```python
# Good: Complex state transitions
class Order:
    def __init__(self):
        self.state = PendingState()

    def process_payment(self):
        self.state.process_payment(self)

    def ship(self):
        self.state.ship(self)

    def cancel(self):
        self.state.cancel(self)

# Many states: Pending -> PaymentProcessed -> Shipped -> Delivered
# Each with different valid transitions and behaviors
```

---

### Template Method Deep Inheritance

**The Problem:**
Creating deep inheritance hierarchies with template methods.

**Bad Example:**
```python
# Anti-pattern: Inheritance hell
class BaseProcessor:
    def process(self):
        self.step1()
        self.step2()
        self.step3()

class IntermediateProcessor(BaseProcessor):
    def step1(self):
        super().step1()
        # Add more

class SpecializedProcessor(IntermediateProcessor):
    def step2(self):
        super().step2()
        # Add more

class VerySpecializedProcessor(SpecializedProcessor):
    def step3(self):
        super().step3()
        # Add more

# Impossible to understand without reading entire hierarchy
```

**Why It's Bad:**
- Tight coupling
- Hard to understand flow
- Fragile base class problem
- Violates composition over inheritance

**Better Approach:**
```python
# Good: Use composition with strategy
class DataProcessor:
    def __init__(self, extractor, transformer, loader):
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def process(self):
        data = self.extractor.extract()
        transformed = self.transformer.transform(data)
        self.loader.load(transformed)

# Flexible composition
processor = DataProcessor(
    CSVExtractor(),
    CleaningTransformer(),
    DatabaseLoader()
)
```

---

## Structural Anti-Patterns

### Decorator Confusion with Inheritance

**The Problem:**
Using inheritance when decoration is needed, or vice versa.

**Bad Example:**
```python
# Anti-pattern: Inheritance explosion
class Coffee:
    def cost(self):
        return 2.00

class CoffeeWithMilk(Coffee):
    def cost(self):
        return 2.50

class CoffeeWithSugar(Coffee):
    def cost(self):
        return 2.25

class CoffeeWithMilkAndSugar(Coffee):
    def cost(self):
        return 2.75

class CoffeeWithMilkAndSugarAndWhippedCream(Coffee):
    def cost(self):
        return 3.25

# Exponential class explosion for combinations
```

**Why It's Bad:**
- Class explosion
- Can't combine features dynamically
- Rigid structure

**Better Approach:**
```python
# Good: Use decorator
class Coffee:
    def cost(self):
        return 2.00

class MilkDecorator:
    def __init__(self, coffee):
        self.coffee = coffee

    def cost(self):
        return self.coffee.cost() + 0.50

class SugarDecorator:
    def __init__(self, coffee):
        self.coffee = coffee

    def cost(self):
        return self.coffee.cost() + 0.25

# Flexible combinations
coffee = Coffee()
coffee = MilkDecorator(coffee)
coffee = SugarDecorator(coffee)
# Can add any combination dynamically
```

---

### Adapter for Control

**The Problem:**
Using Adapter when you control both interfaces.

**Bad Example:**
```python
# Anti-pattern: Unnecessary adapter
class MyClass:
    def my_method(self):
        return "data"

class MyClassAdapter:
    def __init__(self, obj):
        self.obj = obj

    def adapted_method(self):
        return self.obj.my_method()

# Just rename the original method!
```

**Why It's Bad:**
- Unnecessary indirection
- You can just change the interface directly
- More code to maintain

**When Adapter IS Appropriate:**
```python
# Good: Third-party or legacy code
class LegacyPaymentGateway:
    def processPayment(self, amt):  # Can't change this
        # Legacy implementation
        pass

class ModernPaymentAdapter:
    def __init__(self, legacy_gateway):
        self.gateway = legacy_gateway

    def process_payment(self, amount):  # Modern interface
        # Convert to legacy format
        return self.gateway.processPayment(amount * 100)
```

---

### Proxy Without Purpose

**The Problem:**
Creating proxies that don't add any value.

**Bad Example:**
```python
# Anti-pattern: Useless proxy
class ServiceProxy:
    def __init__(self, service):
        self.service = service

    def do_something(self):
        return self.service.do_something()

# Just use the service directly!
```

**Why It's Bad:**
- Adds complexity without benefit
- Extra layer for no reason
- Slows down execution

**When Proxy IS Appropriate:**
```python
# Good: Adds lazy loading
class ImageProxy:
    def __init__(self, filename):
        self.filename = filename
        self.image = None

    def display(self):
        if self.image is None:
            self.image = Image.load(self.filename)  # Load only when needed
        self.image.display()

# Good: Adds access control
class ProtectedDocumentProxy:
    def __init__(self, document, user):
        self.document = document
        self.user = user

    def read(self):
        if self.user.has_permission('read'):
            return self.document.read()
        raise PermissionDenied()
```

---

### Facade as God Object

**The Problem:**
Making facade too large and responsible for too much.

**Bad Example:**
```python
# Anti-pattern: God facade
class ApplicationFacade:
    def create_user(self, data): pass
    def delete_user(self, id): pass
    def update_user(self, id, data): pass
    def create_order(self, data): pass
    def cancel_order(self, id): pass
    def process_payment(self, data): pass
    def send_email(self, to, subject): pass
    def generate_report(self, type): pass
    def export_data(self, format): pass
    def import_data(self, source): pass
    # ... 50 more methods

# Too many responsibilities!
```

**Why It's Bad:**
- Violates Single Responsibility Principle
- Hard to maintain
- Becomes bottleneck for changes
- Defeats purpose of simplification

**Better Approach:**
```python
# Good: Multiple focused facades
class UserManagementFacade:
    def create_user(self, data): pass
    def delete_user(self, id): pass
    def update_user(self, id, data): pass

class OrderFacade:
    def create_order(self, data): pass
    def cancel_order(self, id): pass
    def process_payment(self, data): pass

class ReportingFacade:
    def generate_report(self, type): pass
    def export_data(self, format): pass

# Each facade has focused responsibility
```

---

## General Anti-Patterns

### Pattern Obsession

**The Problem:**
Forcing patterns into code where they don't fit or aren't needed.

**Bad Example:**
```python
# Anti-pattern: Patterns everywhere
class HelloWorldFactory:
    def create_greeter(self):
        return HelloWorldBuilder().set_greeting("Hello").set_target("World").build()

class HelloWorldBuilder:
    def __init__(self):
        self._greeting = None
        self._target = None

    def set_greeting(self, g):
        self._greeting = g
        return self

    def set_target(self, t):
        self._target = t
        return self

    def build(self):
        return Greeter(self._greeting, self._target)

# Just do: print("Hello World")
```

**Why It's Bad:**
- Over-engineering simple problems
- Makes code harder to understand
- Wastes time and effort
- Intimidates other developers

**Right Approach:**
```python
# Use patterns only when they solve real problems
# Simple problem = simple solution
print("Hello World")

# Complex problem = pattern solution
payment_processor = PaymentProcessorFactory.create(config.payment_method)
result = payment_processor.process(order, amount)
```

---

### Premature Pattern Application

**The Problem:**
Applying patterns before understanding if they're needed.

**Key Principles:**
1. **YAGNI** (You Aren't Gonna Need It) - Don't add patterns for hypothetical future needs
2. **KISS** (Keep It Simple, Stupid) - Start simple, refactor to patterns when complexity demands
3. **Refactor to patterns** - It's often better to introduce patterns during refactoring than upfront

**Better Approach:**
1. Write simple code first
2. Identify recurring problems
3. Refactor to patterns when justified
4. Let patterns emerge naturally

---

### Ignoring Python Idioms

**The Problem:**
Implementing patterns from other languages without leveraging Python features.

**Bad Example:**
```python
# Anti-pattern: Ignoring Python's iterator protocol
class CustomIterator:
    def __init__(self, collection):
        self.collection = collection
        self.index = 0

    def has_next(self):
        return self.index < len(self.collection)

    def next(self):
        if self.has_next():
            item = self.collection[self.index]
            self.index += 1
            return item
        raise StopIteration()

# Java-style iteration
iterator = CustomIterator(items)
while iterator.has_next():
    item = iterator.next()
```

**Better - Use Python's Protocol:**
```python
# Good: Pythonic iterator
class CustomIterator:
    def __init__(self, collection):
        self.collection = collection
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.collection):
            raise StopIteration
        item = self.collection[self.index]
        self.index += 1
        return item

# Pythonic usage
for item in CustomIterator(items):
    process(item)
```

**Python Has Built-in Pattern Support:**
- **Iterator**: `__iter__` and `__next__`
- **Context Manager**: `__enter__` and `__exit__` (like Resource Acquisition)
- **Decorator**: `@decorator` syntax
- **Singleton**: Module-level variables
- **Observer**: `property` with getters/setters

---

## Testing Anti-Patterns

### Singleton Testing Nightmares

**The Problem:**
Singleton global state makes tests interdependent.

**Bad Example:**
```python
# Anti-pattern: Tests affect each other
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

def test_user_creation():
    db = DatabaseConnection()
    db.insert_user("Alice")
    # Test passes

def test_user_count():
    db = DatabaseConnection()
    count = db.count_users()
    assert count == 0  # FAILS! Alice still there from previous test
```

**Better Approach:**
```python
# Good: Use dependency injection
class UserService:
    def __init__(self, db):
        self.db = db

def test_user_creation():
    db = MockDatabase()  # Fresh instance
    service = UserService(db)
    service.create_user("Alice")
    assert db.count_users() == 1

def test_user_count():
    db = MockDatabase()  # Fresh instance, independent
    service = UserService(db)
    assert db.count_users() == 0  # PASSES
```

---

## Summary: Warning Signs You're Misusing Patterns

1. **Code is more complex** than before applying the pattern
2. **You can't explain why** you're using a pattern in simple terms
3. **Only one implementation** exists and likely ever will
4. **Tests become harder** to write after applying pattern
5. **New developers are confused** by the code structure
6. **You're using patterns** to look sophisticated rather than solve problems
7. **Simple changes** require touching many files
8. **You're applying patterns** from books without understanding your specific problem

## Golden Rules

1. **Solve the problem first**, then refactor to patterns if needed
2. **Patterns are tools**, not goals - use when they help
3. **Simplicity beats patterns** - if simpler solution exists, use it
4. **Understand the problem** before applying any pattern
5. **Python has idioms** - use them instead of forcing patterns from other languages
6. **Test your decisions** - if pattern makes testing harder, reconsider
7. **Don't be dogmatic** - adapt patterns to your language and context

Remember: The goal is maintainable, understandable code that solves real problems. Patterns are means to that end, not the end itself.
