"""Singleton Pattern Module

The Singleton pattern ensures that a class has only one instance and provides a
global point of access to that instance. This is useful for managing shared resources
like configuration settings, logging, or database connections.

This module demonstrates three implementations:
1. Metaclass-based Singleton (thread-safe)
2. Decorator-based Singleton
3. Module-level Singleton (Pythonic approach)

Example:
    Using the metaclass-based singleton:

    ```python
    class DatabaseConnection(metaclass=SingletonMeta):
        def __init__(self):
            self.connection = "Connected to database"


    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    assert db1 is db2  # True, same instance
    ```
"""

from __future__ import annotations

from threading import Lock
from typing import Any, ClassVar


class SingletonMeta(type):
    """Metaclass that creates a Singleton base class.

    This implementation is thread-safe and ensures that only one instance
    of the class exists across multiple threads.
    """

    _instances: ClassVar[dict[type, Any]] = {}
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

    return get_instance  # type: ignore[return-value]


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
