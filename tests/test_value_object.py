"""Tests for the dataclass versus plain class comparison.

Each test backs a claim made in docs/dataclasses.md, so that the documented
behavior of the decorator cannot drift from what the interpreter does.
"""

import dataclasses
from dataclasses import dataclass, field

import pytest

from design_patterns.structural.value_object import Connection, Point, PointByHand


@pytest.mark.parametrize("cls", [Point, PointByHand])
def test_equal_fields_compare_equal(cls):
    """Two instances with the same field values are equal."""
    assert cls(1.0, 2.0) == cls(1.0, 2.0)


@pytest.mark.parametrize("cls", [Point, PointByHand])
def test_different_fields_compare_unequal(cls):
    """Instances with differing field values are not equal."""
    assert cls(1.0, 2.0) != cls(1.0, 3.0)


@pytest.mark.parametrize("cls", [Point, PointByHand])
def test_second_field_defaults_to_zero(cls):
    """The y field defaults to 0.0 in both versions."""
    assert cls(1.0) == cls(1.0, 0.0)


@pytest.mark.parametrize("cls", [Point, PointByHand])
def test_repr_names_class_and_fields(cls):
    """The repr shows the class name and every field with its value."""
    assert repr(cls(1.0, 2.0)) == f"{cls.__name__}(x=1.0, y=2.0)"


@pytest.mark.parametrize("cls", [Point, PointByHand])
def test_frozen_instances_reject_assignment(cls):
    """Assigning to a field of a frozen instance raises."""
    point = cls(1.0, 2.0)
    with pytest.raises(AttributeError):
        point.x = 5.0


@pytest.mark.parametrize("cls", [Point, PointByHand])
def test_frozen_instances_are_usable_as_set_members(cls):
    """Equal frozen instances collapse to one set member."""
    assert len({cls(1.0, 2.0), cls(1.0, 2.0), cls(3.0)}) == 2


def test_different_classes_with_equal_fields_are_not_equal():
    """The generated __eq__ compares class identity before field values."""
    assert Point(1.0, 2.0) != PointByHand(1.0, 2.0)


def test_dataclass_records_its_fields():
    """The decorator records field metadata that introspection helpers use."""
    assert [f.name for f in dataclasses.fields(Point)] == ["x", "y"]
    assert dataclasses.asdict(Point(1.0, 2.0)) == {"x": 1.0, "y": 2.0}
    assert dataclasses.replace(Point(1.0, 2.0), y=9.0) == Point(1.0, 9.0)


def test_connections_compare_by_identity():
    """A plain class keeps identity semantics: equal fields, distinct objects."""
    first = Connection("db")
    second = Connection("db")
    assert first.host == second.host
    assert first != second
    assert first == first


def test_mutable_default_is_rejected_at_class_creation():
    """A bare list default would be shared by every instance, so it is refused."""
    with pytest.raises(ValueError, match="mutable default"):

        @dataclass
        class Bag:
            items: list[int] = []  # noqa: RUF008 - the rejection is the point


def test_default_factory_gives_each_instance_its_own_value():
    """default_factory is the sanctioned way to get a per-instance mutable."""

    @dataclass
    class Bag:
        items: list[int] = field(default_factory=list)

    first, second = Bag(), Bag()
    first.items.append(1)
    assert second.items == []


def test_required_field_cannot_follow_default_field():
    """The generated __init__ is positional, so ordering is enforced."""
    with pytest.raises(TypeError, match="non-default argument"):
        dataclasses.make_dataclass("Misordered", [("x", float, 0.0), ("y", float)])


def test_kw_only_lifts_the_ordering_restriction():
    """Keyword-only fields have no positional order to violate."""

    @dataclass(kw_only=True)
    class Ordered:
        x: float = 0.0
        y: float

    assert Ordered(y=1.0) == Ordered(x=0.0, y=1.0)


def test_mutable_dataclass_with_eq_is_unhashable():
    """Value equality without immutability disables hashing."""

    @dataclass
    class Mutable:
        x: float

    assert Mutable.__hash__ is None
    with pytest.raises(TypeError, match="unhashable"):
        hash(Mutable(1.0))
