# Singleton Pattern

**Category:** Creational Pattern

## Intent

Ensure a class has only one instance and provide a global point of access to it. The Singleton pattern restricts instantiation of a class to a single object, which is useful for managing shared resources like configuration settings, logging, or database connections.

## Problem

When you need to ensure that only one instance of a class exists throughout the application lifecycle, direct instantiation leads to:

- Multiple instances being created accidentally
- Inconsistent state across different parts of the application
- Difficulty managing shared resources
- Race conditions in multi-threaded environments
- No global access point to the single instance

## When to Use

Use the Singleton pattern when:

- **Single instance required**: Only one instance of a class should exist in the system
- **Global access needed**: The instance needs to be accessible from anywhere in the application
- **Shared resources**: Managing resources like database connections, thread pools, or caches
- **Configuration management**: Centralized configuration that must be consistent across the application
- **Logging**: Single logging instance that all components use
- **Lazy initialization**: The expensive object should only be created when first needed

## When NOT to Use

Avoid the Singleton pattern when:

- **Testing difficulties**: Singletons make unit testing harder due to global state
- **Tight coupling**: Creates hidden dependencies throughout the codebase
- **Concurrent access**: Complex synchronization needed for thread-safe access
- **Flexibility**: You might need multiple instances in the future
- **Dependency injection preferred**: Modern frameworks handle instance management better
- **Global state issues**: Singletons introduce global state which can cause problems

## Structure

The Singleton pattern involves:

- **Singleton Class**: Maintains a single instance and provides a global access point
- **Private Constructor**: Prevents direct instantiation from outside the class
- **Static Instance**: Holds the single instance of the class
- **Thread Safety**: Ensures thread-safe creation in multi-threaded environments

## Implementation

### Metaclass-Based Singleton

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

### Decorator-Based Singleton

```python
def singleton_decorator(cls: type) -> type:
    """Decorator that converts a class into a singleton.

    Args:
        cls: The class to convert into a singleton.

    Returns:
        A wrapper class that implements singleton behavior.
    """
    instances: dict[type, Any] = {}
    lock = Lock()

    def get_instance(*args: Any, **kwargs: Any) -> Any:
        """Get or create the singleton instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The singleton instance.
        """
        with lock:
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton_decorator
class Logger:
    """Example singleton logger class using decorator pattern.

    This logger ensures all parts of the application use the same logging instance.
    """

    def __init__(self) -> None:
        """Initialize the logger."""
        self.logs: list[str] = []

    def log(self, message: str) -> None:
        """Log a message.

        Args:
            message: The message to log.
        """
        self.logs.append(message)

    def get_logs(self) -> list[str]:
        """Get all logged messages.

        Returns:
            List of all logged messages.
        """
        return self.logs
```

### __new__ Method Singleton

```python
class ConfigurationManager:
    """Pythonic singleton using class attributes.

    This implementation uses a class attribute to store the single instance,
    which is a common Python idiom for singletons.
    """

    _instance: ConfigurationManager | None = None
    _lock: Lock = Lock()

    def __new__(cls) -> ConfigurationManager:
        """Create or return the singleton instance.

        Returns:
            The singleton instance.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Initialize the configuration manager."""
        if self._initialized:
            return
        self.config: dict[str, Any] = {}
        self._initialized = True

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.

        Args:
            key: The configuration key.
            value: The configuration value.
        """
        self.config[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: The configuration key.
            default: Default value if key not found.

        Returns:
            The configuration value or default.
        """
        return self.config.get(key, default)
```

## Usage Example

```python
# Metaclass-based singleton
db1 = DatabaseConnection()
db2 = DatabaseConnection()
assert db1 is db2  # True - same instance
print(db1.execute_query("SELECT * FROM users"))

# Decorator-based singleton
logger1 = Logger()
logger2 = Logger()
assert logger1 is logger2  # True - same instance
logger1.log("Application started")
print(logger2.get_logs())  # Shows the log from logger1

# __new__ method singleton
config1 = ConfigurationManager()
config2 = ConfigurationManager()
assert config1 is config2  # True - same instance
config1.set("theme", "dark")
print(config2.get("theme"))  # Output: dark
```

## Key Benefits

1. **Controlled access**: Single point of control over the sole instance
2. **Reduced namespace pollution**: Avoids global variables while providing global access
3. **Lazy initialization**: Instance created only when first needed
4. **Thread safety**: Proper implementation ensures safe concurrent access
5. **Consistent state**: Single instance ensures consistent state across the application
6. **Resource management**: Efficient management of shared resources

## Drawbacks

1. **Global state**: Introduces global state which can make code harder to reason about
2. **Testing difficulties**: Hard to mock or replace in unit tests
3. **Hidden dependencies**: Classes depending on singletons have hidden dependencies
4. **Tight coupling**: Can lead to tightly coupled code
5. **Concurrency issues**: Requires careful synchronization in multi-threaded environments
6. **Violation of SRP**: Class manages both its business logic and instance lifecycle
7. **Subclassing difficulties**: Hard to subclass without breaking singleton behavior

## Real-World Examples

- **Logging systems**: Single logger instance used throughout application
- **Configuration managers**: Centralized configuration accessible everywhere
- **Database connection pools**: Single pool managing multiple connections
- **Cache managers**: Shared cache instance across application
- **Thread pools**: Single pool managing worker threads
- **Device drivers**: Single driver instance controlling hardware
- **Application state**: Global state manager for application settings
- **Resource managers**: File handle managers, socket pools

## Related Patterns

- **Factory Method**: Can use Singleton to ensure factory is a single instance
- **Abstract Factory**: Factory implementations are often singletons
- **Facade**: Facade objects are often implemented as singletons
- **State**: State objects can be shared singletons
- **Flyweight**: Uses singleton-like approach for shared objects

## API Reference

::: design_patterns.creational.singleton
    options:
      show_root_heading: true
      show_source: true
