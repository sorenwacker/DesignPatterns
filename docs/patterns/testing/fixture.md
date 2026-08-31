# Fixture

**Category:** Testing Pattern

## Overview

A fixture provides a fixed baseline state for tests to run against. Fixtures encapsulate test setup and teardown logic, enabling reusable test data and environment configuration. This pattern separates test preparation from test assertions, improving test clarity and reducing duplication.

## Concepts

### Test Fixture

Setup and teardown mechanism that establishes a known state before each test runs and optionally cleans up afterward. Commonly implemented through lifecycle methods (`setUp`/`tearDown`) or dependency injection (pytest fixtures).

### Data Fixture

Predefined data sets used to populate databases, configure services, or provide sample inputs. Data fixtures ensure tests run against consistent, predictable data.

### Object Mother / Test Data Builder

Factory patterns specialized for creating complex test objects with sensible defaults. Object Mother provides static factory methods, while Test Data Builder uses a fluent interface for customization.

## Usage Guidelines

**Use when:**

- Multiple tests require the same setup or test data
- Test setup logic is complex enough to obscure test intent
- Tests need isolation from external dependencies (databases, APIs)
- You want to share test infrastructure across a test suite

**Avoid when:**

- Each test has unique setup requirements with no overlap
- Tests are simple enough that inline setup improves readability
- The fixture abstraction hides important test context
- Setup/teardown overhead exceeds the benefit for trivial tests

## Implementation

### Test Fixture (Context Manager)

```python
from contextlib import contextmanager
from dataclasses import dataclass, field
from collections.abc import Generator
from typing import Any


@dataclass
class FixtureContext:
    """Container for test state managed by a fixture."""
    data: dict[str, Any] = field(default_factory=dict)
    resources: list[Any] = field(default_factory=list)


@contextmanager
def database_fixture() -> Generator[FixtureContext, None, None]:
    """Fixture that sets up and tears down a test database connection."""
    context = FixtureContext()
    # Setup: create test database connection
    context.data["db"] = {"connected": True, "tables": []}
    context.resources.append("db_connection")

    try:
        yield context
    finally:
        # Teardown: close connection and cleanup
        context.data["db"]["connected"] = False
        context.resources.clear()
```

### Data Fixture

```python
from dataclasses import dataclass


@dataclass
class User:
    """Domain object representing a user."""
    id: int
    name: str
    email: str
    role: str = "user"


class UserFixtures:
    """Predefined user data for testing."""

    @staticmethod
    def admin_user() -> User:
        """Returns a standard admin user for testing."""
        return User(id=1, name="Admin", email="admin@example.com", role="admin")

    @staticmethod
    def regular_user() -> User:
        """Returns a standard regular user for testing."""
        return User(id=2, name="John Doe", email="john@example.com", role="user")

    @staticmethod
    def users_list() -> list[User]:
        """Returns a list of test users."""
        return [
            UserFixtures.admin_user(),
            UserFixtures.regular_user(),
            User(id=3, name="Jane Doe", email="jane@example.com"),
        ]
```

### Test Data Builder

```python
from dataclasses import dataclass


@dataclass
class Order:
    """Domain object representing an order."""
    id: int
    customer_id: int
    items: list[str]
    total: float
    status: str


class OrderBuilder:
    """Fluent builder for creating Order test objects with sensible defaults."""

    def __init__(self) -> None:
        self._id: int = 1
        self._customer_id: int = 100
        self._items: list[str] = ["default_item"]
        self._total: float = 0.0
        self._status: str = "pending"

    def with_id(self, order_id: int) -> "OrderBuilder":
        """Set the order ID."""
        self._id = order_id
        return self

    def with_customer(self, customer_id: int) -> "OrderBuilder":
        """Set the customer ID."""
        self._customer_id = customer_id
        return self

    def with_items(self, items: list[str]) -> "OrderBuilder":
        """Set the order items. The list is copied, so later edits by the caller do not reach the order."""
        self._items = list(items)
        return self

    def with_total(self, total: float) -> "OrderBuilder":
        """Set the order total."""
        self._total = total
        return self

    def with_status(self, status: str) -> "OrderBuilder":
        """Set the order status."""
        self._status = status
        return self

    def completed(self) -> "OrderBuilder":
        """Configure as a completed order."""
        self._status = "completed"
        return self

    def build(self) -> Order:
        """Build and return the Order instance."""
        return Order(
            id=self._id,
            customer_id=self._customer_id,
            items=self._items,
            total=self._total,
            status=self._status,
        )
```

### Usage

```python
# Test Fixture usage
with database_fixture() as ctx:
    assert ctx.data["db"]["connected"] is True
    # Run tests with database context
# After context exits, connection is closed

# Data Fixture usage
admin = UserFixtures.admin_user()
assert admin.role == "admin"

all_users = UserFixtures.users_list()
assert len(all_users) == 3

# Test Data Builder usage
order = (
    OrderBuilder()
    .with_customer(42)
    .with_items(["widget", "gadget"])
    .with_total(99.99)
    .completed()
    .build()
)
assert order.status == "completed"
assert order.customer_id == 42
```

## Trade-offs

**Benefits:**

1. Reduces test code duplication through reusable setup logic
2. Improves test readability by separating setup from assertions
3. Ensures consistent test data across the test suite
4. Test Data Builder allows creating complex objects with minimal boilerplate

**Drawbacks:**

1. Adds indirection that may obscure what data a test uses
2. Shared fixtures can create hidden dependencies between tests
3. Overly generic fixtures may not fit specific test requirements
4. Fixture maintenance overhead increases as the test suite grows

## Real-World Examples

- pytest fixtures for database connections and mock services
- Django TestCase with `setUp()` and `tearDown()` methods
- Factory libraries (factory_boy, Faker) for generating test data
- Database seeding scripts for integration tests

## Related Patterns

- Factory (fixtures often use factories internally)
- Builder (Test Data Builder is a specialized application)
- Singleton (shared fixtures may use singleton semantics)
- Template Method (fixture lifecycle follows template pattern)

## API Reference

::: design_patterns.testing.fixture
    options:
      show_root_heading: true
      show_source: true
