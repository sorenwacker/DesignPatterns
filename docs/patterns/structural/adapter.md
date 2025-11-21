# Adapter Pattern

**Category:** Structural Pattern

## Intent

Convert the interface of a class into another interface clients expect. The Adapter pattern allows classes to work together that couldn't otherwise because of incompatible interfaces. It acts as a bridge between two incompatible interfaces.

## Problem

When you need to use existing classes with incompatible interfaces, direct usage leads to:

- Inability to reuse existing classes
- Tight coupling to specific interfaces
- Code duplication to work around interface mismatches
- Difficulty integrating legacy code
- No way to make third-party libraries work with your code

## When to Use

Use the Adapter pattern when:

- **Incompatible interfaces**: Want to use class with incompatible interface
- **Legacy integration**: Need to integrate legacy code with new systems
- **Third-party libraries**: Library interface doesn't match your needs
- **Multiple adaptees**: Want to provide uniform interface to related classes
- **Interface translation**: Need to translate between different interfaces
- **Reuse existing**: Want to reuse existing class without modification

## When NOT to Use

Avoid the Adapter pattern when:

- **Compatible interfaces**: Interfaces are already compatible
- **Modify source**: Can modify the original class interface
- **Simple wrapper**: A simple wrapper function suffices
- **Performance critical**: Adapter overhead is unacceptable
- **Overkill**: Pattern adds unnecessary complexity

## Structure

The Adapter pattern involves:

- **Target**: Interface that client expects
- **Adaptee**: Existing class with incompatible interface
- **Adapter**: Converts adaptee interface to target interface
- **Client**: Works with target interface

## Implementation

### Logger Adapter Example

```python
class LoggerInterface:
    """The target interface that clients will use.

    This interface defines the logging methods that the application expects.
    """
    def log_info(self, message: str) -> None:
        """Logs an informational message.

        Args:
            message: The message to log as informational.
        """
        raise NotImplementedError

    def log_error(self, message: str) -> None:
        """Logs an error message.

        Args:
            message: The message to log as an error.
        """
        raise NotImplementedError

class LegacyLogger:
    """A legacy logging system.

    This class represents an existing logging system that has its own interface.
    It logs messages to the console.
    """
    def write_log(self, message: str) -> None:
        """Writes a log message.

        Args:
            message: The log message to write.
        """
        print(f"Legacy Log: {message}")

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

    def log_info(self, message: str) -> None:
        """Logs an informational message using the legacy logger.

        Args:
            message: The message to log as informational.
        """
        self._legacy_logger.write_log(f"INFO: {message}")

    def log_error(self, message: str) -> None:
        """Logs an error message using the legacy logger.

        Args:
            message: The message to log as an error.
        """
        self._legacy_logger.write_log(f"ERROR: {message}")
```

## Usage Example

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

## Key Benefits

1. **Reusability**: Reuse existing classes with incompatible interfaces
2. **Single Responsibility**: Separates interface conversion from business logic
3. **Flexibility**: Can adapt multiple incompatible classes
4. **Open/Closed Principle**: Introduce new adapters without changing existing code
5. **Legacy integration**: Makes legacy code work with new systems
6. **Third-party compatibility**: Makes third-party libraries compatible

## Drawbacks

1. **Complexity**: Adds extra classes and indirection
2. **Performance**: Additional layer adds overhead
3. **Confusion**: Can make code harder to understand
4. **Multiple adapters**: Many adapters can clutter codebase
5. **Maintenance**: More classes to maintain

## Real-World Examples

- **Database adapters**: Adapting different database drivers to common interface
- **Payment gateways**: Adapting different payment providers to unified interface
- **File format converters**: Converting between different file formats
- **API wrappers**: Wrapping REST APIs with object-oriented interfaces
- **Hardware drivers**: Adapting hardware interfaces to software interfaces
- **Logging libraries**: Adapting different logging frameworks
- **Cloud storage**: Adapting AWS S3, Google Cloud Storage to common interface

## Related Patterns

- **Bridge**: Separates abstraction from implementation, Adapter makes incompatible interfaces work
- **Decorator**: Adds behavior, Adapter changes interface
- **Facade**: Simplifies interface, Adapter changes interface
- **Proxy**: Provides same interface, Adapter changes interface

## API Reference

::: design_patterns.structural.adapter
    options:
      show_root_heading: true
      show_source: true
