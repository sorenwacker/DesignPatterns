# Builder Pattern

**Category:** Creational Pattern

## Intent

Separate the construction of a complex object from its representation, allowing the same construction process to create different representations. The Builder pattern provides a step-by-step approach to constructing objects, particularly useful when objects require many configuration parameters or complex initialization.

## Problem

Creating complex objects with many optional parameters leads to:

- Constructor telescoping with numerous parameters
- Confusion about parameter order and meaning
- Difficulty creating different representations of the same object
- Immutable objects being hard to construct
- Code duplication in object creation logic
- Poor readability when creating objects

## When to Use

Use the Builder pattern when:

- **Complex construction**: Object creation involves many steps or configuration options
- **Multiple representations**: Same construction process should create different representations
- **Fluent interface desired**: Method chaining provides better readability
- **Optional parameters**: Many optional parameters would lead to multiple constructors
- **Immutable objects**: Building immutable objects step by step before finalization
- **Director pattern**: Construction process can be abstracted and reused

## When NOT to Use

Avoid the Builder pattern when:

- **Simple objects**: Object has few parameters and simple construction
- **Fixed construction**: Object always created the same way
- **Performance critical**: Builder adds overhead with intermediate objects
- **Single representation**: Only one way to construct the object
- **Dataclass sufficient**: Python dataclasses or named tuples work well

## Structure

The Builder pattern involves:

- **Builder**: Interface for creating parts of a Product
- **Concrete Builder**: Implements builder interface and constructs/assembles parts
- **Product**: Complex object being constructed
- **Director** (optional): Encapsulates construction logic for common configurations
- **Fluent Interface**: Method chaining for better readability

## Implementation

### Computer Builder Example

```python
from __future__ import annotations

class Computer:
    """Represents a computer with various components.

    This is the product class that the builder constructs.
    """

    def __init__(self) -> None:
        """Initialize an empty computer."""
        self.cpu: str | None = None
        self.ram: int | None = None
        self.storage: str | None = None
        self.gpu: str | None = None
        self.os: str | None = None
        self.peripherals: list[str] = []

    def get_specifications(self) -> str:
        """Get the computer specifications as a formatted string.

        Returns:
            A string representation of the computer specifications.
        """
        specs = []
        if self.cpu:
            specs.append(f"CPU: {self.cpu}")
        if self.ram:
            specs.append(f"RAM: {self.ram}GB")
        if self.storage:
            specs.append(f"Storage: {self.storage}")
        if self.gpu:
            specs.append(f"GPU: {self.gpu}")
        if self.os:
            specs.append(f"OS: {self.os}")
        if self.peripherals:
            specs.append(f"Peripherals: {', '.join(self.peripherals)}")
        return "\n".join(specs) if specs else "No specifications set"

class ComputerBuilder:
    """Builder for constructing Computer objects.

    This builder uses method chaining (fluent interface) to set component properties.
    """

    def __init__(self) -> None:
        """Initialize the builder with a new Computer instance."""
        self._computer = Computer()

    def set_cpu(self, cpu: str) -> ComputerBuilder:
        """Set the CPU.

        Args:
            cpu: The CPU model.

        Returns:
            The builder instance for method chaining.
        """
        self._computer.cpu = cpu
        return self

    def set_ram(self, ram: int) -> ComputerBuilder:
        """Set the RAM amount in GB.

        Args:
            ram: The RAM size in gigabytes.

        Returns:
            The builder instance for method chaining.
        """
        self._computer.ram = ram
        return self

    def set_storage(self, storage: str) -> ComputerBuilder:
        """Set the storage configuration.

        Args:
            storage: The storage description.

        Returns:
            The builder instance for method chaining.
        """
        self._computer.storage = storage
        return self

    def set_gpu(self, gpu: str) -> ComputerBuilder:
        """Set the GPU.

        Args:
            gpu: The GPU model.

        Returns:
            The builder instance for method chaining.
        """
        self._computer.gpu = gpu
        return self

    def set_os(self, os: str) -> ComputerBuilder:
        """Set the operating system.

        Args:
            os: The operating system name.

        Returns:
            The builder instance for method chaining.
        """
        self._computer.os = os
        return self

    def add_peripheral(self, peripheral: str) -> ComputerBuilder:
        """Add a peripheral device.

        Args:
            peripheral: The peripheral name.

        Returns:
            The builder instance for method chaining.
        """
        self._computer.peripherals.append(peripheral)
        return self

    def build(self) -> Computer:
        """Build and return the configured Computer instance.

        Returns:
            The fully constructed Computer instance.
        """
        return self._computer

    def reset(self) -> ComputerBuilder:
        """Reset the builder to start building a new computer.

        Returns:
            The builder instance with a new Computer.
        """
        self._computer = Computer()
        return self
```

### House Builder with Director Methods

```python
class House:
    """Represents a house with various features.

    This demonstrates an alternative product for the builder pattern.
    """

    def __init__(self) -> None:
        """Initialize an empty house."""
        self.foundation: str | None = None
        self.walls: str | None = None
        self.roof: str | None = None
        self.windows: int = 0
        self.doors: int = 0
        self.garage: bool = False
        self.garden: bool = False

    def describe(self) -> str:
        """Get a description of the house.

        Returns:
            A string describing the house features.
        """
        features = []
        if self.foundation:
            features.append(f"Foundation: {self.foundation}")
        if self.walls:
            features.append(f"Walls: {self.walls}")
        if self.roof:
            features.append(f"Roof: {self.roof}")
        features.append(f"Windows: {self.windows}")
        features.append(f"Doors: {self.doors}")
        if self.garage:
            features.append("Has garage")
        if self.garden:
            features.append("Has garden")
        return ", ".join(features) if features else "Empty house"

class HouseBuilder:
    """Builder for constructing House objects.

    This demonstrates director methods that encapsulate common build configurations.
    """

    def __init__(self) -> None:
        """Initialize the builder with a new House instance."""
        self._house = House()

    def set_foundation(self, foundation: str) -> HouseBuilder:
        """Set the foundation type."""
        self._house.foundation = foundation
        return self

    def set_walls(self, walls: str) -> HouseBuilder:
        """Set the wall material."""
        self._house.walls = walls
        return self

    def set_roof(self, roof: str) -> HouseBuilder:
        """Set the roof type."""
        self._house.roof = roof
        return self

    def set_windows(self, count: int) -> HouseBuilder:
        """Set the number of windows."""
        self._house.windows = count
        return self

    def set_doors(self, count: int) -> HouseBuilder:
        """Set the number of doors."""
        self._house.doors = count
        return self

    def add_garage(self) -> HouseBuilder:
        """Add a garage to the house."""
        self._house.garage = True
        return self

    def add_garden(self) -> HouseBuilder:
        """Add a garden to the house."""
        self._house.garden = True
        return self

    def build(self) -> House:
        """Build and return the configured House instance."""
        return self._house

    def build_simple_house(self) -> House:
        """Build a simple house with basic features.

        This is a director method that encapsulates a common configuration.
        """
        return (self
                .set_foundation("Concrete slab")
                .set_walls("Brick")
                .set_roof("Asphalt shingles")
                .set_windows(4)
                .set_doors(1)
                .build())

    def build_luxury_house(self) -> House:
        """Build a luxury house with premium features.

        This is a director method that encapsulates a premium configuration.
        """
        return (self
                .set_foundation("Deep foundation")
                .set_walls("Stone")
                .set_roof("Tile")
                .set_windows(12)
                .set_doors(3)
                .add_garage()
                .add_garden()
                .build())
```

## Usage Example

```python
# Building a custom computer
builder = ComputerBuilder()
computer = (builder
            .set_cpu("Intel i9")
            .set_ram(32)
            .set_storage("1TB SSD")
            .set_gpu("NVIDIA RTX 4090")
            .set_os("Windows 11")
            .add_peripheral("Mechanical Keyboard")
            .add_peripheral("Gaming Mouse")
            .build())

print(computer.get_specifications())
# Output:
# CPU: Intel i9
# RAM: 32GB
# Storage: 1TB SSD
# GPU: NVIDIA RTX 4090
# OS: Windows 11
# Peripherals: Mechanical Keyboard, Gaming Mouse

# Using director methods for common configurations
house_builder = HouseBuilder()
simple_house = house_builder.build_simple_house()
print(simple_house.describe())

# Build luxury house
luxury_house = HouseBuilder().build_luxury_house()
print(luxury_house.describe())
```

## Key Benefits

1. **Readable code**: Fluent interface makes construction code clear and self-documenting
2. **Step-by-step construction**: Build complex objects incrementally
3. **Different representations**: Same builder can create different product variants
4. **Encapsulation**: Construction details hidden from client code
5. **Immutable products**: Can construct immutable objects piece by piece
6. **Director pattern**: Common configurations can be encapsulated in director methods
7. **Single Responsibility**: Separates construction logic from business logic

## Drawbacks

1. **Increased complexity**: Adds extra classes and code
2. **Code duplication**: Builder methods may duplicate product setters
3. **Overhead**: Creates intermediate objects during construction
4. **Not always needed**: Overkill for simple objects
5. **Incomplete objects**: Product may be in invalid state during construction
6. **Mutability**: Builder typically creates mutable intermediate states

## Real-World Examples

- **SQL query builders**: Constructing complex queries step by step
- **HTTP request builders**: Building requests with headers, body, parameters
- **Document builders**: Creating documents with various sections and formatting
- **UI builders**: Constructing complex UI components
- **Test data builders**: Creating test objects with various configurations
- **Configuration builders**: Building application configurations
- **String builders**: Efficiently constructing strings (StringBuilder in Java)
- **Form builders**: Building forms with various fields and validations

## Related Patterns

- **Abstract Factory**: Builder focuses on constructing complex objects step by step, Factory creates products in one call
- **Composite**: Builder can construct Composite trees
- **Prototype**: Can use builder to configure prototype before cloning
- **Singleton**: Builder itself is often a singleton
- **Fluent Interface**: Builder commonly uses fluent interface design

## API Reference

::: design_patterns.creational.builder
    options:
      show_root_heading: true
      show_source: true
