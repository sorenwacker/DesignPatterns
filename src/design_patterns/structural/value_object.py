"""Dataclass versus plain class.

`Point` and `PointByHand` are the same class written two ways: the first lets
`@dataclass` generate `__init__`, `__repr__`, `__eq__`, `__hash__`, and the
frozen `__setattr__`; the second writes them out. `Connection` shows the case
the decorator does not fit: an object whose meaning is its identity, not its
field values. See docs/dataclasses.md for when to choose which.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    """A coordinate pair that compares by value.

    Attributes:
        x (float): Horizontal coordinate.
        y (float): Vertical coordinate, defaulting to the axis.
    """

    x: float
    y: float = 0.0


class PointByHand:
    """`Point` with every method the decorator would generate written out.

    Attributes:
        x (float): Horizontal coordinate.
        y (float): Vertical coordinate, defaulting to the axis.
    """

    x: float
    y: float

    def __init__(self, x: float, y: float = 0.0) -> None:
        """Assign the fields, bypassing the frozen `__setattr__`."""
        object.__setattr__(self, "x", x)
        object.__setattr__(self, "y", y)

    def __repr__(self) -> str:
        """Show the class name and every field with its value."""
        return f"PointByHand(x={self.x!r}, y={self.y!r})"

    def __eq__(self, other: object) -> bool:
        """Compare field-wise, but only against the same class."""
        if other.__class__ is not self.__class__:
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self) -> int:
        """Hash the fields as a tuple, consistent with `__eq__`."""
        return hash((self.x, self.y))

    def __setattr__(self, name: str, value: object) -> None:
        """Refuse assignment after construction."""
        message = f"cannot assign to field {name!r}"
        raise AttributeError(message)


class Connection:
    """A connection to a host, meaningful by identity rather than by value.

    Two connections to the same host are two connections, so this class keeps
    the default identity-based `__eq__` and `__hash__`.

    Attributes:
        host (str): The host this connection is open to.
    """

    def __init__(self, host: str) -> None:
        """Open a connection to the given host."""
        self.host = host
