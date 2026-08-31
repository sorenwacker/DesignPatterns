"""Tests for the Singleton pattern."""

import inspect
import threading

import pytest

from design_patterns.creational.singleton import (
    ConfigurationManager,
    DatabaseConnection,
    Logger,
    SingletonMeta,
)


@pytest.fixture(autouse=True)
def fresh_singletons():
    """Forget every instance so no test observes another test's state.

    Yields:
        dict[type, Any]: The metaclass registry, empty at the start of the test.
    """
    SingletonMeta._instances.clear()
    ConfigurationManager._instance = None
    yield SingletonMeta._instances
    SingletonMeta._instances.clear()
    ConfigurationManager._instance = None


def test_each_test_starts_without_instances(fresh_singletons):
    """The reset is what makes the state assertions below order-independent."""
    assert fresh_singletons == {}
    assert ConfigurationManager._instance is None


def test_database_connection_singleton():
    """Test that DatabaseConnection returns the same instance."""
    assert DatabaseConnection() is DatabaseConnection()


def test_database_connection_state_shared():
    """Test that singleton state is shared across instances."""
    DatabaseConnection().execute_query("SELECT * FROM users")
    assert DatabaseConnection().queries_executed == 1


def test_logger_singleton():
    """Test that Logger returns the same instance."""
    assert Logger() is Logger()


def test_logger_is_still_a_class():
    """The decorator must return a class, so isinstance and subclassing work."""
    assert inspect.isclass(Logger)
    assert isinstance(Logger(), Logger)
    assert Logger.__name__ == "Logger"


def test_logger_initialises_once():
    """A second call must not re-run __init__ and wipe the shared state."""
    Logger().log("First message")
    Logger().log("Second message")
    assert Logger().get_logs() == ["First message", "Second message"]


def test_configuration_manager_singleton():
    """Test that ConfigurationManager returns the same instance."""
    assert ConfigurationManager() is ConfigurationManager()


def test_configuration_manager_state_shared():
    """Test that configuration manager state is shared."""
    ConfigurationManager().set("debug", True)
    assert ConfigurationManager().get("debug") is True


def test_singleton_thread_safety():
    """Test that singleton is thread-safe."""
    instances = []

    def create_instance():
        instances.append(DatabaseConnection())

    threads = [threading.Thread(target=create_instance) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert all(instance is instances[0] for instance in instances)


def test_configuration_manager_initialization():
    """Test that ConfigurationManager initializes only once."""
    ConfigurationManager().set("key1", "value1")
    assert ConfigurationManager().get("key1") == "value1"
    assert ConfigurationManager()._initialized is True


def test_database_connection_exposes_its_connection_string():
    """Test that the singleton connection reports its connection string."""
    assert DatabaseConnection().connection_string == "Connected to database"
