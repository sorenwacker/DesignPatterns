"""Tests for the Singleton pattern."""

import threading

from design_patterns.creational.singleton import (
    ConfigurationManager,
    DatabaseConnection,
    Logger,
)


def test_database_connection_singleton():
    """Test that DatabaseConnection returns the same instance."""
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    assert db1 is db2


def test_database_connection_state_shared():
    """Test that singleton state is shared across instances."""
    db1 = DatabaseConnection()
    db1.execute_query("SELECT * FROM users")

    db2 = DatabaseConnection()
    assert db2.queries_executed == 1


def test_logger_singleton():
    """Test that Logger returns the same instance."""
    logger1 = Logger()
    logger2 = Logger()
    assert logger1 is logger2


def test_logger_state_shared():
    """Test that logger state is shared."""
    logger1 = Logger()
    logger1.log("First message")

    logger2 = Logger()
    logger2.log("Second message")

    assert len(logger1.get_logs()) == 2
    assert logger2.get_logs() == logger1.get_logs()


def test_configuration_manager_singleton():
    """Test that ConfigurationManager returns the same instance."""
    config1 = ConfigurationManager()
    config2 = ConfigurationManager()
    assert config1 is config2


def test_configuration_manager_state_shared():
    """Test that configuration manager state is shared."""
    config1 = ConfigurationManager()
    config1.set("debug", True)

    config2 = ConfigurationManager()
    assert config2.get("debug") is True


def test_singleton_thread_safety():
    """Test that singleton is thread-safe."""
    instances = []

    def create_instance():
        db = DatabaseConnection()
        instances.append(db)

    threads = [threading.Thread(target=create_instance) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert all(instance is instances[0] for instance in instances)


def test_configuration_manager_initialization():
    """Test that ConfigurationManager initializes only once."""
    config1 = ConfigurationManager()
    config1.set("key1", "value1")

    config2 = ConfigurationManager()
    assert config2.get("key1") == "value1"
    assert config1._initialized is True
    assert config2._initialized is True


def test_database_connection_exposes_its_connection_string():
    """Test that the singleton connection reports its connection string."""
    connection = DatabaseConnection()

    assert connection.connection_string == "Connected to database"
