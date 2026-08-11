"""Tests for the Fixture pattern."""

import pytest

from design_patterns.testing.fixture import (
    FixtureContext,
    Order,
    OrderBuilder,
    User,
    UserFixtures,
    database_fixture,
)


class TestFixtureContextClass:
    """Tests for FixtureContext dataclass."""

    def test_default_initialization(self):
        """Test that FixtureContext initializes with empty data and resources."""
        ctx = FixtureContext()
        assert ctx.data == {}
        assert ctx.resources == []

    def test_data_can_be_set(self):
        """Test that data dictionary can store values."""
        ctx = FixtureContext()
        ctx.data["key"] = "value"
        assert ctx.data["key"] == "value"

    def test_resources_can_be_appended(self):
        """Test that resources list can store items."""
        ctx = FixtureContext()
        ctx.resources.append("resource1")
        ctx.resources.append("resource2")
        assert len(ctx.resources) == 2
        assert "resource1" in ctx.resources


class TestDatabaseFixture:
    """Tests for database_fixture context manager."""

    def test_setup_creates_connection(self):
        """Test that fixture sets up database connection on entry."""
        with database_fixture() as ctx:
            assert ctx.data["db"]["connected"] is True
            assert ctx.data["db"]["tables"] == []
            assert "db_connection" in ctx.resources

    def test_teardown_closes_connection(self):
        """Test that fixture closes connection on exit."""
        with database_fixture() as ctx:
            pass
        assert ctx.data["db"]["connected"] is False
        assert ctx.resources == []

    def test_teardown_on_exception(self):
        """Test that fixture cleans up even when exception occurs."""
        ctx_ref = None
        with pytest.raises(ValueError):
            with database_fixture() as ctx:
                ctx_ref = ctx
                raise ValueError("Test exception")
        assert ctx_ref.data["db"]["connected"] is False
        assert ctx_ref.resources == []


class TestUser:
    """Tests for User dataclass."""

    def test_user_creation(self):
        """Test User can be created with required fields."""
        user = User(id=1, name="Test", email="test@example.com")
        assert user.id == 1
        assert user.name == "Test"
        assert user.email == "test@example.com"
        assert user.role == "user"

    def test_user_with_custom_role(self):
        """Test User can be created with custom role."""
        user = User(id=1, name="Admin", email="admin@example.com", role="admin")
        assert user.role == "admin"


class TestUserFixtures:
    """Tests for UserFixtures data fixtures."""

    def test_admin_user(self):
        """Test admin_user returns expected admin user."""
        admin = UserFixtures.admin_user()
        assert admin.id == 1
        assert admin.name == "Admin"
        assert admin.email == "admin@example.com"
        assert admin.role == "admin"

    def test_regular_user(self):
        """Test regular_user returns expected regular user."""
        user = UserFixtures.regular_user()
        assert user.id == 2
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.role == "user"

    def test_users_list(self):
        """Test users_list returns list of users."""
        users = UserFixtures.users_list()
        assert len(users) == 3
        assert users[0].role == "admin"
        assert users[1].role == "user"
        assert users[2].name == "Jane Doe"


class TestOrder:
    """Tests for Order dataclass."""

    def test_order_creation(self):
        """Test Order can be created with all fields."""
        order = Order(
            id=1, customer_id=100, items=["item1"], total=50.0, status="pending"
        )
        assert order.id == 1
        assert order.customer_id == 100
        assert order.items == ["item1"]
        assert order.total == 50.0
        assert order.status == "pending"


class TestOrderBuilder:
    """Tests for OrderBuilder Test Data Builder."""

    def test_default_values(self):
        """Test builder creates order with default values."""
        order = OrderBuilder().build()
        assert order.id == 1
        assert order.customer_id == 100
        assert order.items == ["default_item"]
        assert order.total == 0.0
        assert order.status == "pending"

    def test_with_id(self):
        """Test builder can set custom id."""
        order = OrderBuilder().with_id(42).build()
        assert order.id == 42

    def test_with_customer(self):
        """Test builder can set custom customer."""
        order = OrderBuilder().with_customer(999).build()
        assert order.customer_id == 999

    def test_with_items(self):
        """Test builder can set custom items."""
        items = ["widget", "gadget"]
        order = OrderBuilder().with_items(items).build()
        assert order.items == items

    def test_with_total(self):
        """Test builder can set custom total."""
        order = OrderBuilder().with_total(99.99).build()
        assert order.total == 99.99

    def test_with_status(self):
        """Test builder can set custom status."""
        order = OrderBuilder().with_status("shipped").build()
        assert order.status == "shipped"

    def test_completed_shorthand(self):
        """Test completed() sets status to completed."""
        order = OrderBuilder().completed().build()
        assert order.status == "completed"

    def test_fluent_chaining(self):
        """Test builder methods can be chained."""
        order = (
            OrderBuilder()
            .with_id(5)
            .with_customer(42)
            .with_items(["product"])
            .with_total(25.0)
            .completed()
            .build()
        )
        assert order.id == 5
        assert order.customer_id == 42
        assert order.items == ["product"]
        assert order.total == 25.0
        assert order.status == "completed"
