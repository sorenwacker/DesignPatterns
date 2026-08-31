# Dataclasses vs Plain Classes

A `@dataclass` is a plain class with boilerplate generated for it. It still runs `__init__`, still has a `__dict__`, still supports inheritance, methods, and properties. The decorator reads the class-level annotations, in declaration order, and writes the methods a value-like class always needs into the class. Nothing else changes.

## Usage Guidelines

### When to use

- The class is primarily a bundle of named values and two instances with the same field values should compare equal. Configuration objects, result records, AST nodes, coordinates, money amounts.
- Instances are constructed by assigning arguments to attributes with no side effects. That is exactly the `__init__` the decorator generates.
- You want a readable `repr` and field-wise equality without maintaining them by hand as fields are added.
- The object should be immutable and usable as a dictionary key or set member. `frozen=True` gives both.
- In pattern terms: Memento state snapshots, Command parameter objects, Builder output, Flyweight intrinsic state, and value objects in general.

### When not to use

- Identity is the meaning. Two `Connection` objects to the same host are not the same connection. The generated `__eq__` is wrong for such classes and would have to be disabled with `eq=False`, at which point the decorator adds little.
- Construction is not "assign the arguments". An `__init__` that opens a resource, validates against external state, or takes arguments that do not map one-to-one to attributes is clearer written by hand than expressed through `field(init=False)` and `__post_init__`.
- The class is mostly behavior with little state: a Strategy, a Visitor, a Handler in a chain. There is nothing for the decorator to generate.
- You need a custom `__hash__` and `__eq__` relationship that the decorator's rules fight against.
- The value must be validated or parsed on every construction from untrusted input. Use a validating model such as `pydantic.BaseModel` at the I/O boundary and a dataclass for the internal representation.

## Implementation

The decorated class and the hand-written class below are equivalent. Both are in `design_patterns.structural.value_object`, and the test suite asserts that they behave the same.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: float
    y: float = 0.0
```

Written out by hand, `Point` is:

```python
class PointByHand:
    def __init__(self, x: float, y: float = 0.0) -> None:
        object.__setattr__(self, "x", x)
        object.__setattr__(self, "y", y)

    def __repr__(self) -> str:
        return f"PointByHand(x={self.x!r}, y={self.y!r})"

    def __eq__(self, other: object) -> bool:
        if other.__class__ is not self.__class__:
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __setattr__(self, name: str, value: object) -> None:
        message = f"cannot assign to field {name!r}"
        raise AttributeError(message)
```

A class whose instances have identity rather than value stays a plain class:

```python
class Connection:
    def __init__(self, host: str) -> None:
        self.host = host
```

Two `Connection("db")` instances are distinct objects, and `==` says so because the default `object.__eq__` compares identity.

## Decorator Options

| Option | Effect |
|--------|--------|
| `order=True` | Generates `__lt__`, `__le__`, `__gt__`, `__ge__` comparing fields as tuples |
| `frozen=True` | Assignment raises `FrozenInstanceError`; instances become hashable |
| `slots=True` | Generates `__slots__`; smaller instances and faster attribute access |
| `kw_only=True` | All fields are keyword-only in `__init__` |
| `field(default_factory=list)` | Per-instance mutable default; a bare `= []` is rejected |
| `field(init=False)`, `repr=False`, `compare=False` | Exclude a field from the corresponding generated method |
| `__post_init__` | Hook that runs after `__init__` for validation or derived fields |
| `asdict`, `astuple`, `replace`, `fields` | Introspection helpers that work because field metadata is recorded on the class |

## Pitfalls

- A mutable default such as `items: list = []` raises `ValueError` when the class is created. Use `field(default_factory=list)`.
- A field without a default cannot follow a field with a default, because the generated `__init__` is positional. `kw_only=True` lifts this restriction.
- Base class fields come first in the generated `__init__`, so a base with defaults and a subclass with a required field hits the ordering error above.
- `eq=True` without `frozen=True` sets `__hash__` to `None`. Instances become unhashable. This is correct, since a mutable object that compares by value must not hash, but it surprises code that puts instances in sets.
- `frozen=True` is enforced through `__setattr__`, so `object.__setattr__(self, name, value)` inside `__post_init__` is the sanctioned way to set derived fields.
- A class-level annotation without a default declares a field, not a class attribute. Annotate with `ClassVar[T]` to declare a class attribute.

## Related Tools

- `typing.NamedTuple`: immutable and tuple-based. Lighter than a frozen dataclass, but tuple behavior leaks: `Point(1, 2) == (1, 2)` is `True` and unpacking works whether or not it is intended.
- `attrs`: the library dataclasses were modeled on. Adds validators and converters.
- `pydantic.BaseModel`: dataclass-like declaration with runtime validation and parsing. Suited to I/O boundaries; the validation cost is paid on every construction.
