"""
Factory Pattern Example: Logger System

Demonstrates using the Factory pattern to create different types of loggers
based on configuration, without coupling the client code to specific logger implementations.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


class Logger(ABC):
    """Abstract logger interface"""

    @abstractmethod
    def log(self, message: str) -> None:
        pass


class ConsoleLogger(Logger):
    """Logs messages to console"""

    def log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[CONSOLE {timestamp}] {message}")


class FileLogger(Logger):
    """Logs messages to a file"""

    def __init__(self, filename: str = "app.log"):
        self.filename = filename
        self.messages: List[str] = []

    def log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[FILE {timestamp}] {message}"
        self.messages.append(log_entry)
        print(f"Logged to {self.filename}: {log_entry}")


class DatabaseLogger(Logger):
    """Logs messages to a database (simulated)"""

    def __init__(self):
        self.logs: List[tuple] = []

    def log(self, message: str) -> None:
        timestamp = datetime.now()
        self.logs.append((timestamp, message))
        print(f"[DATABASE {timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {message}")


class LoggerFactory:
    """Factory for creating logger instances"""

    @staticmethod
    def create_logger(logger_type: str, **kwargs) -> Logger:
        """
        Create a logger based on type.

        Args:
            logger_type: Type of logger ('console', 'file', or 'database')
            **kwargs: Additional arguments for specific logger types

        Returns:
            Logger instance

        Raises:
            ValueError: If logger type is unknown
        """
        if logger_type == "console":
            return ConsoleLogger()
        elif logger_type == "file":
            filename = kwargs.get("filename", "app.log")
            return FileLogger(filename)
        elif logger_type == "database":
            return DatabaseLogger()
        else:
            raise ValueError(f"Unknown logger type: {logger_type}")


def main():
    """Demonstrate the Factory pattern with different logger types"""

    print("=" * 60)
    print("Factory Pattern: Logger System")
    print("=" * 60)

    # Configuration could come from environment variables, config files, etc.
    # For this demo, we'll use different types

    print("\n1. Console Logger:")
    console_logger = LoggerFactory.create_logger("console")
    console_logger.log("Application started")
    console_logger.log("User logged in")

    print("\n2. File Logger:")
    file_logger = LoggerFactory.create_logger("file", filename="debug.log")
    file_logger.log("Debug: Processing request")
    file_logger.log("Debug: Request completed")

    print("\n3. Database Logger:")
    db_logger = LoggerFactory.create_logger("database")
    db_logger.log("Critical: Database connection lost")
    db_logger.log("Info: Database connection restored")

    # The factory makes it easy to switch logger types
    print("\n4. Runtime Configuration:")
    config = {"log_type": "console", "environment": "production"}

    logger = LoggerFactory.create_logger(config["log_type"])
    logger.log(f"Application running in {config['environment']} mode")

    # Easy to add new logger types without modifying client code
    print("\n5. Error Handling:")
    try:
        invalid_logger = LoggerFactory.create_logger("network")
    except ValueError as e:
        print(f"Error: {e}")

    print("\n" + "=" * 60)
    print("Benefits of Factory Pattern:")
    print("- Centralized object creation")
    print("- Easy to switch implementations")
    print("- Client code doesn't depend on concrete classes")
    print("- New logger types can be added without changing client code")
    print("=" * 60)


if __name__ == "__main__":
    main()
