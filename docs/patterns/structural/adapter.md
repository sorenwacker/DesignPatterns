# Adapter Pattern

**Category:** Structural Pattern

## Overview

Convert the interface of a class into another interface clients expect. This pattern allows classes to work together that couldn't otherwise because of incompatible interfaces, acting as a bridge between two incompatible interfaces.

## Usage Guidelines

**Use when:**

- Want to use class with incompatible interface
- Need to integrate legacy code with new systems
- Library interface doesn't match your needs
- Want to provide uniform interface to related classes

**Avoid when:**

- Interfaces are already compatible
- Can modify the original class interface
- A simple wrapper function suffices
- Pattern adds unnecessary complexity

## Implementation

```python
from abc import ABC, abstractmethod

class LoggerInterface(ABC):
    """The target interface that clients will use.

    This interface defines the logging methods that the application expects.
    """
    @abstractmethod
    def log_info(self, message: str) -> str:
        """Logs an informational message.

        Args:
            message: The message to log as informational.
        """

    @abstractmethod
    def log_error(self, message: str) -> str:
        """Logs an error message.

        Args:
            message: The message to log as an error.
        """

class LegacyLogger:
    """A legacy logging system.

    This class represents an existing logging system that has its own interface.
    It has its own line format.
    """
    def write_log(self, message: str) -> str:
        """Writes a log message and returns the formatted line.

        Args:
            message: The log message to write.
        """
        return f"Legacy Log: {message}"

class LoggerAdapter(LoggerInterface):
    """An adapter for the legacy logger.

    This adapter adapts the LegacyLogger to the LoggerInterface, allowing
    the application to use the legacy logging system through the new interface.
    """

    def __init__(self, legacy_logger: LegacyLogger):
        """Initializes the LoggerAdapter with a legacy logger.

        Args:
            legacy_logger: An instance of the legacy logger.
        """
        self._legacy_logger = legacy_logger

    def log_info(self, message: str) -> str:
        """Logs an informational message using the legacy logger.

        Args:
            message: The message to log as informational.
        """
        return self._legacy_logger.write_log(f"INFO: {message}")

    def log_error(self, message: str) -> str:
        """Logs an error message using the legacy logger.

        Args:
            message: The message to log as an error.
        """
        return self._legacy_logger.write_log(f"ERROR: {message}")
```

### Usage

```python
# Create legacy logger
legacy_logger = LegacyLogger()

# Adapt it to new interface
logger = LoggerAdapter(legacy_logger)

# Use with new interface
logger.log_info("This is an informational message.")
# Output: Legacy Log: INFO: This is an informational message.

logger.log_error("This is an error message.")
# Output: Legacy Log: ERROR: This is an error message.
```

## Trade-offs

**Benefits:**

1. Reuse existing classes with incompatible interfaces
2. Separates interface conversion from business logic (Single Responsibility)
3. Can adapt multiple incompatible classes
4. Introduce new adapters without changing existing code (Open/Closed Principle)

**Drawbacks:**

1. Adds extra classes and indirection increasing complexity
2. Additional layer adds performance overhead
3. Can make code harder to understand
4. Many adapters can clutter codebase

## Real-World Examples

- Database adapters for different database drivers
- Payment gateways adapting different providers
- File format converters
- API wrappers for REST APIs

## Related Patterns

- Bridge
- Decorator
- Facade
- Proxy

## API Reference

::: design_patterns.structural.adapter
    options:
      show_root_heading: true
      show_source: true
