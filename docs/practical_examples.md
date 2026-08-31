# Practical Examples - Real-World Use Cases

This guide shows how design patterns solve real-world problems with concrete examples from actual software systems.

## Web Application Scenarios

### Factory Pattern - Database Connection Management

```python
# Problem: Need to create different database connections based on configuration
class DatabaseConnectionFactory:
    @staticmethod
    def create_connection(db_type: str):
        if db_type == "postgres":
            return PostgreSQLConnection()
        elif db_type == "mysql":
            return MySQLConnection()
        elif db_type == "sqlite":
            return SQLiteConnection()
        raise ValueError(f"Unknown database type: {db_type}")

# Usage: Easy to switch databases via configuration
db = DatabaseConnectionFactory.create_connection(config.get("DB_TYPE"))
```

**Real Usage:** Django ORM, SQLAlchemy, connection pooling libraries

---

### Singleton Pattern - Application Configuration

```python
from design_patterns.creational.singleton import ConfigurationManager

# Problem: Application needs one global configuration accessible everywhere
config = ConfigurationManager()
config.set("api_key", "secret-key")
config.set("debug", True)

# Anywhere in the application:
config = ConfigurationManager()  # Returns same instance
api_key = config.get("api_key")
```

**Real Usage:** Flask app config, Django settings, logging configuration

---

### Builder Pattern - HTTP Request Construction

```python
from design_patterns.creational.builder import ComputerBuilder

# Problem: HTTP requests have many optional parameters
class HTTPRequestBuilder:
    def __init__(self):
        self._request = HTTPRequest()

    def set_url(self, url):
        self._request.url = url
        return self

    def set_method(self, method):
        self._request.method = method
        return self

    def add_header(self, key, value):
        self._request.headers[key] = value
        return self

    def set_body(self, body):
        self._request.body = body
        return self

    def build(self):
        return self._request

# Usage: Clean, readable request construction
request = (HTTPRequestBuilder()
           .set_url("https://api.example.com/users")
           .set_method("POST")
           .add_header("Content-Type", "application/json")
           .add_header("Authorization", "Bearer token")
           .set_body({"name": "John"})
           .build())
```

**Real Usage:** Requests library, aiohttp, RestKit

---

### Observer Pattern - Event System

```python
from design_patterns.behavioral.observer import WeatherStation, PhoneDisplay

# Problem: User actions should trigger multiple UI updates
class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type, callback):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event_type, data):
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                callback(data)

# Usage: Decouple event sources from handlers
bus = EventBus()
bus.subscribe("user_registered", send_welcome_email)
bus.subscribe("user_registered", update_analytics)
bus.subscribe("user_registered", notify_admins)

# Trigger all handlers with one call
bus.publish("user_registered", {"email": "user@example.com"})
```

**Real Usage:** Django signals, Flask signals, JavaScript event systems

---

### Strategy Pattern - Payment Processing

```python
from design_patterns.behavioral.strategy import ShoppingCart, CreditCardPayment

# Problem: Support multiple payment methods without tight coupling
class PaymentProcessor:
    def __init__(self):
        self._strategy = None

    def set_payment_method(self, strategy):
        self._strategy = strategy

    def process_payment(self, amount):
        return self._strategy.pay(amount)

# Usage: Easy to add new payment methods
processor = PaymentProcessor()

# Credit card payment
processor.set_payment_method(CreditCardPayment("1234-5678"))
processor.process_payment(99.99)

# Switch to PayPal at runtime
processor.set_payment_method(PayPalPayment("user@email.com"))
processor.process_payment(49.99)
```

**Real Usage:** Stripe, PayPal SDKs, e-commerce platforms

---

### Decorator Pattern - Middleware

```python
from design_patterns.structural.decorator import SimpleCoffee, MilkDecorator

# Problem: Need to add cross-cutting concerns to request handling
def authentication_middleware(handler):
    def wrapper(request):
        if not request.user.is_authenticated:
            raise Unauthorized("Login required")
        return handler(request)
    return wrapper

def logging_middleware(handler):
    def wrapper(request):
        print(f"Request: {request.method} {request.path}")
        response = handler(request)
        print(f"Response: {response.status_code}")
        return response
    return wrapper

def rate_limit_middleware(handler):
    def wrapper(request):
        if rate_limiter.is_exceeded(request.user):
            raise TooManyRequests()
        return handler(request)
    return wrapper

# Usage: Stack decorators for layered behavior
@authentication_middleware
@logging_middleware
@rate_limit_middleware
def api_endpoint(request):
    return {"data": "response"}
```

**Real Usage:** Django middleware, Flask before_request, Express.js middleware

---

### Proxy Pattern - Lazy Loading ORM

```python
from design_patterns.structural.proxy import ImageProxy

# Problem: Loading related objects from database is expensive
class UserProfileProxy:
    def __init__(self, user_id):
        self.user_id = user_id
        self._profile = None

    def get_profile(self):
        if self._profile is None:
            # Only query database when actually needed
            self._profile = database.query(Profile).filter(user_id=self.user_id).first()
        return self._profile

# Usage: Avoid N+1 query problems
users = database.query(User).all()
for user in users:
    # Profile only loaded if accessed
    if some_condition:
        print(user.profile.bio)  # Database query happens here
```

**Real Usage:** Django ORM select_related, SQLAlchemy lazy loading, Hibernate

---

## Microservices Scenarios

### Facade Pattern - Service Layer

```python
from design_patterns.structural.facade import HomeTheaterFacade

# Problem: Complex operations across multiple microservices
class OrderFacade:
    def __init__(self):
        self.inventory_service = InventoryService()
        self.payment_service = PaymentService()
        self.shipping_service = ShippingService()
        self.notification_service = NotificationService()

    def place_order(self, order_data):
        # Simplify complex workflow
        inventory_check = self.inventory_service.check_availability(order_data.items)

        if not inventory_check.available:
            raise OutOfStock()

        payment = self.payment_service.charge(order_data.payment_info)
        self.inventory_service.reserve_items(order_data.items)
        shipping = self.shipping_service.create_shipment(order_data)
        self.notification_service.send_confirmation(order_data.email)

        return {"order_id": payment.order_id, "tracking": shipping.tracking_number}

# Usage: Simple interface for complex operation
facade = OrderFacade()
result = facade.place_order(order_data)
```

**Real Usage:** API gateways, BFF (Backend for Frontend) pattern

---

### Mediator Pattern - Service Bus

```python
from design_patterns.behavioral.mediator import ChatRoom

# Problem: Services need to communicate without direct coupling
class ServiceMediator:
    def __init__(self):
        self._services = {}
        self._event_handlers = {}

    def register_service(self, name, service):
        self._services[name] = service

    def send_event(self, event_type, data):
        # Route events between services
        if event_type in self._event_handlers:
            for handler in self._event_handlers[event_type]:
                handler(data)

# Usage: Decouple microservices
mediator = ServiceMediator()
mediator.register_service("orders", OrderService())
mediator.register_service("inventory", InventoryService())
mediator.register_service("notifications", NotificationService())

# Order service publishes event
mediator.send_event("order_placed", order_data)

# Multiple services react independently
```

**Real Usage:** RabbitMQ, Kafka, AWS EventBridge, Azure Service Bus

---

## Data Processing Scenarios

### Iterator Pattern - Large Dataset Processing

```python
from design_patterns.behavioral.iterator import BookCollection

# Problem: Process large datasets without loading everything into memory
class ChunkedDataIterator:
    def __init__(self, query, chunk_size=1000):
        self.query = query
        self.chunk_size = chunk_size
        self.offset = 0

    def __iter__(self):
        return self

    def __next__(self):
        chunk = self.query.limit(self.chunk_size).offset(self.offset).all()
        if not chunk:
            raise StopIteration
        self.offset += self.chunk_size
        return chunk

# Usage: Memory-efficient processing
for chunk in ChunkedDataIterator(User.query, chunk_size=500):
    process_users(chunk)  # Process 500 users at a time
```

**Real Usage:** Pandas chunking, database cursor pagination, ETL pipelines

---

### Visitor Pattern - AST Processing

```python
from design_patterns.behavioral.visitor import AreaCalculator

# Problem: Perform different operations on syntax tree nodes
class CodeOptimizer:
    def visit_binary_op(self, node):
        # Optimize: x * 1 => x
        if node.operator == "*" and node.right == 1:
            return node.left
        return node

    def visit_if_statement(self, node):
        # Optimize: if True: => just body
        if node.condition.is_constant() and node.condition.value:
            return node.then_branch
        return node

# Usage: Separate algorithm from data structure
optimizer = CodeOptimizer()
optimized_ast = ast.accept(optimizer)
```

**Real Usage:** Compilers, linters (pylint, mypy), code formatters (black)

---

### Template Method Pattern - Data Pipeline

```python
from design_patterns.behavioral.template_method import DataMiner

# Problem: ETL pipelines share common structure
class DataPipeline:
    def run(self):
        # Template method defining process
        data = self.extract()
        transformed = self.transform(data)
        self.load(transformed)
        self.cleanup()

    def extract(self):
        raise NotImplementedError

    def transform(self, data):
        raise NotImplementedError

    def load(self, data):
        raise NotImplementedError

    def cleanup(self):
        pass  # Hook method with default

class CSVToDatabase(DataPipeline):
    def extract(self):
        return pd.read_csv("data.csv")

    def transform(self, data):
        return data.dropna().fillna(0)

    def load(self, data):
        data.to_sql("table", engine)

# Usage: Consistent pipeline structure
pipeline = CSVToDatabase()
pipeline.run()
```

**Real Usage:** Apache Airflow DAGs, Luigi pipelines, Prefect workflows

---

## State Management Scenarios

### Memento Pattern - Undo System

```python
from design_patterns.behavioral.memento import TextEditor, History

# Problem: Implement undo/redo for complex state
class DocumentEditor:
    def __init__(self):
        self.content = ""
        self.cursor_position = 0
        self.selection = None
        self._history = []
        self._redo_stack = []

    def save_state(self):
        state = {
            "content": self.content,
            "cursor": self.cursor_position,
            "selection": self.selection
        }
        self._history.append(state)
        self._redo_stack.clear()

    def undo(self):
        if self._history:
            current = self.get_state()
            self._redo_stack.append(current)
            previous = self._history.pop()
            self.restore_state(previous)

    def redo(self):
        if self._redo_stack:
            current = self.get_state()
            self._history.append(current)
            next_state = self._redo_stack.pop()
            self.restore_state(next_state)

# Usage: Full undo/redo support
editor = DocumentEditor()
editor.insert_text("Hello")
editor.save_state()
editor.insert_text(" World")
editor.save_state()
editor.undo()  # Back to "Hello"
editor.redo()  # Forward to "Hello World"
```

**Real Usage:** Text editors, graphic editors, game state management

---

### State Pattern - Order Processing

```python
from design_patterns.behavioral.state import Document

# Problem: Complex state transitions with different behavior
class OrderState:
    def process_payment(self, order):
        raise NotImplementedError

    def ship(self, order):
        raise NotImplementedError

    def cancel(self, order):
        raise NotImplementedError

class PendingState(OrderState):
    def process_payment(self, order):
        order.state = PaymentProcessedState()
        return "Payment processed"

    def cancel(self, order):
        order.state = CancelledState()
        return "Order cancelled"

class PaymentProcessedState(OrderState):
    def ship(self, order):
        order.state = ShippedState()
        return "Order shipped"

# Usage: Clear state transitions
order = Order()
order.process_payment()  # Pending -> PaymentProcessed
order.ship()             # PaymentProcessed -> Shipped
```

**Real Usage:** E-commerce order systems, workflow engines, game state machines

---

## Testing Scenarios

### Abstract Factory Pattern - Test Fixtures

```python
from design_patterns.creational.abstract_factory import GUIFactory

# Problem: Create consistent test data across different scenarios
class TestFixtureFactory:
    def create_user(self):
        raise NotImplementedError

    def create_order(self):
        raise NotImplementedError

class ValidDataFactory(TestFixtureFactory):
    def create_user(self):
        return User(email="valid@test.com", age=25)

    def create_order(self):
        return Order(total=100, status="pending")

class InvalidDataFactory(TestFixtureFactory):
    def create_user(self):
        return User(email="invalid", age=-5)

    def create_order(self):
        return Order(total=-100, status="invalid")

# Usage: Easy test data creation
def test_valid_user():
    factory = ValidDataFactory()
    user = factory.create_user()
    assert user.is_valid()

def test_invalid_user():
    factory = InvalidDataFactory()
    user = factory.create_user()
    assert not user.is_valid()
```

**Real Usage:** pytest fixtures, factory_boy, faker

---

## Performance Optimization Scenarios

### Prototype Pattern - Object Pooling

```python
from design_patterns.creational.prototype import Document

# Problem: Creating database connections is expensive
class ConnectionPool:
    def __init__(self, size=10):
        self._available = []
        self._in_use = set()

        # Create prototype connection
        prototype = DatabaseConnection()

        # Clone prototype instead of creating new connections
        for _ in range(size):
            self._available.append(prototype.clone())

    def acquire(self):
        if not self._available:
            raise NoAvailableConnections()
        conn = self._available.pop()
        self._in_use.add(conn)
        return conn

    def release(self, conn):
        self._in_use.remove(conn)
        conn.reset()  # Reset to clean state
        self._available.append(conn)

# Usage: Reuse expensive objects
pool = ConnectionPool(size=5)
conn = pool.acquire()
conn.execute("SELECT * FROM users")
pool.release(conn)  # Return to pool for reuse
```

**Real Usage:** Database connection pools, thread pools, object pools

---

## Key Takeaways

1. **Patterns solve recurring problems** - Each example shows a real problem patterns address
2. **Context matters** - Same pattern solves different problems in different domains
3. **Patterns combine** - Real systems often use multiple patterns together
4. **Simplicity first** - Only use patterns when they solve actual complexity
5. **Python idioms** - Some patterns are built into Python (decorators, iterators, context managers)
