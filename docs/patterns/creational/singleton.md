# Singleton Pattern

**Category:** Creational Pattern

## Overview

Ensure a class has only one instance and provide a global point of access to it. This pattern restricts instantiation of a class to a single object, useful for managing shared resources like configuration settings, logging, or database connections.

## Usage Guidelines

**Use when:**
- Only one instance of a class should exist in the system
- The instance needs to be accessible from anywhere in the application
- Managing shared resources like database connections, thread pools, or caches
- Centralized configuration that must be consistent across the application

**Avoid when:**
- Singletons make unit testing harder due to global state
- Creates hidden dependencies throughout the codebase
- Complex synchronization needed for thread-safe access
- You might need multiple instances in the future

## Implementation

```python
from threading import Lock
from typing import Any

class SingletonMeta(type):
    """Metaclass that creates a Singleton base class.

    This implementation is thread-safe and ensures that only one instance
    of the class exists across multiple threads.
    """

    _instances: dict[type, Any] = {}
    _lock: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Create or return the singleton instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The singleton instance of the class.
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

class DatabaseConnection(metaclass=SingletonMeta):
    """Example singleton class representing a database connection.

    This class can only have one instance throughout the application lifecycle.
    """

    def __init__(self) -> None:
        """Initialize the database connection."""
        self.connection_string = "Connected to database"
        self.queries_executed = 0

    def execute_query(self, query: str) -> str:
        """Execute a database query.

        Args:
            query: The SQL query to execute.

        Returns:
            Result message indicating query execution.
        """
        self.queries_executed += 1
        return f"Executed: {query}"
```

### Usage

```python
# Metaclass-based singleton
db1 = DatabaseConnection()
db2 = DatabaseConnection()
assert db1 is db2  # True - same instance
print(db1.execute_query("SELECT * FROM users"))
```

## Trade-offs

**Benefits:**
1. Controlled access through single point of control
2. Reduced namespace pollution while providing global access
3. Lazy initialization with instance created only when first needed
4. Thread safety with proper implementation ensuring safe concurrent access

**Drawbacks:**
1. Introduces global state making code harder to reason about
2. Hard to mock or replace in unit tests
3. Classes depending on singletons have hidden dependencies
4. Requires careful synchronization in multi-threaded environments

## Real-World Examples

- Logging systems used throughout application
- Configuration managers centrally accessible
- Database connection pools
- Cache managers shared across application

## Related Patterns

- Factory Method
- Abstract Factory
- Facade
- State
- Flyweight

## API Reference

::: design_patterns.creational.singleton
    options:
      show_root_heading: true
      show_source: true
