"""
Fixture pattern implementations for testing.

This module provides three complementary approaches to test fixtures:

1. FixtureContext / context manager fixtures: Manage setup and teardown of test state
2. Data Fixtures: Provide predefined test data through static factory methods
3. Test Data Builder: Create complex test objects with fluent interface

These patterns help reduce test code duplication, improve readability, and ensure
consistent test data across a test suite.
"""

from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any


@dataclass
class FixtureContext:
    """Container for test state managed by a fixture.

    Attributes:
        data: Dictionary holding arbitrary test data and state.
        resources: List of resources that need cleanup after the test.

    Example:
        ```python
        ctx = FixtureContext()
        ctx.data["connection"] = create_connection()
        ctx.resources.append(ctx.data["connection"])
        ```
    """

    data: dict[str, Any] = field(default_factory=dict)
    resources: list[Any] = field(default_factory=list)


@contextmanager
def database_fixture() -> Generator[FixtureContext, None, None]:
    """Context manager fixture that sets up and tears down a test database connection.

    Yields:
        FixtureContext: Context containing simulated database connection state.

    Example:
        ```python
        with database_fixture() as ctx:
            assert ctx.data["db"]["connected"] is True
            # Run database tests here
        # Connection automatically closed after context exits
        ```
    """
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


@dataclass
class User:
    """Domain object representing a user.

    Attributes:
        id: Unique user identifier.
        name: User's display name.
        email: User's email address.
        role: User's role (defaults to "user").
    """

    id: int
    name: str
    email: str
    role: str = "user"


class UserFixtures:
    """Predefined user data for testing.

    Provides static factory methods that return User instances with
    predetermined values, ensuring consistent test data.

    Example:
        ```python
        admin = UserFixtures.admin_user()
        assert admin.role == "admin"
        ```
    """

    @staticmethod
    def admin_user() -> User:
        """Returns a standard admin user for testing.

        Returns:
            User: Admin user with id=1, role="admin".
        """
        return User(id=1, name="Admin", email="admin@example.com", role="admin")

    @staticmethod
    def regular_user() -> User:
        """Returns a standard regular user for testing.

        Returns:
            User: Regular user with id=2, role="user".
        """
        return User(id=2, name="John Doe", email="john@example.com", role="user")

    @staticmethod
    def users_list() -> list[User]:
        """Returns a list of test users.

        Returns:
            list[User]: List containing admin, regular user, and additional user.
        """
        return [
            UserFixtures.admin_user(),
            UserFixtures.regular_user(),
            User(id=3, name="Jane Doe", email="jane@example.com"),
        ]


@dataclass
class Order:
    """Domain object representing an order.

    Attributes:
        id: Unique order identifier.
        customer_id: ID of the customer who placed the order.
        items: List of item names in the order.
        total: Total price of the order.
        status: Current order status.
    """

    id: int
    customer_id: int
    items: list[str]
    total: float
    status: str


class OrderBuilder:
    """Fluent builder for creating Order test objects with sensible defaults.

    Implements the Test Data Builder pattern, allowing tests to specify only
    the attributes relevant to the test while using reasonable defaults
    for everything else.

    Example:
        ```python
        order = (
            OrderBuilder()
            .with_customer(42)
            .with_items(["widget", "gadget"])
            .completed()
            .build()
        )
        assert order.customer_id == 42
        assert order.status == "completed"
        ```
    """

    def __init__(self) -> None:
        """Initialize builder with default values."""
        self._id: int = 1
        self._customer_id: int = 100
        self._items: list[str] = ["default_item"]
        self._total: float = 0.0
        self._status: str = "pending"

    def with_id(self, order_id: int) -> "OrderBuilder":
        """Set the order ID.

        Args:
            order_id: The order identifier.

        Returns:
            OrderBuilder: Self for method chaining.
        """
        self._id = order_id
        return self

    def with_customer(self, customer_id: int) -> "OrderBuilder":
        """Set the customer ID.

        Args:
            customer_id: The customer identifier.

        Returns:
            OrderBuilder: Self for method chaining.
        """
        self._customer_id = customer_id
        return self

    def with_items(self, items: list[str]) -> "OrderBuilder":
        """Set the order items.

        Args:
            items: List of item names.

        Returns:
            OrderBuilder: Self for method chaining.
        """
        self._items = list(items)
        return self

    def with_total(self, total: float) -> "OrderBuilder":
        """Set the order total.

        Args:
            total: The total price.

        Returns:
            OrderBuilder: Self for method chaining.
        """
        self._total = total
        return self

    def with_status(self, status: str) -> "OrderBuilder":
        """Set the order status.

        Args:
            status: The order status string.

        Returns:
            OrderBuilder: Self for method chaining.
        """
        self._status = status
        return self

    def completed(self) -> "OrderBuilder":
        """Configure as a completed order.

        Returns:
            OrderBuilder: Self for method chaining.
        """
        self._status = "completed"
        return self

    def build(self) -> Order:
        """Build and return the Order instance.

        Returns:
            Order: The constructed Order object.
        """
        return Order(
            id=self._id,
            customer_id=self._customer_id,
            items=list(self._items),
            total=self._total,
            status=self._status,
        )
