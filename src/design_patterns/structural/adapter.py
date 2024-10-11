"""
Adapter Pattern Example

This module demonstrates the Adapter Pattern, which allows incompatible interfaces to work together.
In this example, a legacy logging system is adapted to conform to a new logging interface.

Classes:
    LoggerInterface: The target interface that clients will use.
    LegacyLogger: A legacy logging system that writes logs to the console.
    LoggerAdapter: An adapter that allows the legacy logging system to be used with the new interface.

Usage:
    Create an instance of `LegacyLogger` and wrap it with `LoggerAdapter`. Then use the adapter
    to log messages using the `log_info` and `log_error` methods.

Example:
    ```
    legacy_logger = LegacyLogger()
    logger = LoggerAdapter(legacy_logger)
    logger.log_info("This is an informational message.")
    > Legacy Log: INFO: This is an informational message.
    
    logger.log_error("This is an error message.")
    > Legacy Log: ERROR: This is an error message.
    ```
"""

class LoggerInterface:
    """The target interface that clients will use.

    This interface defines the logging methods that the application expects.
    """
    def log_info(self, message: str) -> None:
        """Logs an informational message.

        Args:
            message (str): The message to log as informational.
        """
        raise NotImplementedError

    def log_error(self, message: str) -> None:
        """Logs an error message.

        Args:
            message (str): The message to log as an error.
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
            message (str): The log message to write.
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
            legacy_logger (LegacyLogger): An instance of the legacy logger.
        """
        self._legacy_logger = legacy_logger

    def log_info(self, message: str) -> None:
        """Logs an informational message using the legacy logger.

        Args:
            message (str): The message to log as informational.
        """
        self._legacy_logger.write_log(f"INFO: {message}")

    def log_error(self, message: str) -> None:
        """Logs an error message using the legacy logger.

        Args:
            message (str): The message to log as an error.
        """
        self._legacy_logger.write_log(f"ERROR: {message}")
