"""Builder Pattern Module

The Builder pattern separates the construction of a complex object from its
representation, allowing the same construction process to create different
representations. It is particularly useful when an object requires many
configuration parameters or when the construction process involves multiple steps.

Example:
    Building a computer with various components:

    ```python
    builder = ComputerBuilder()
    computer = (
        builder.set_cpu("Intel i9")
        .set_ram(32)
        .set_storage("1TB SSD")
        .set_gpu("NVIDIA RTX 4090")
        .build()
    )

    print(computer.get_specifications())
    ```
"""

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
        """Set the foundation type.

        Args:
            foundation: The foundation type.

        Returns:
            The builder instance for method chaining.
        """
        self._house.foundation = foundation
        return self

    def set_walls(self, walls: str) -> HouseBuilder:
        """Set the wall material.

        Args:
            walls: The wall material.

        Returns:
            The builder instance for method chaining.
        """
        self._house.walls = walls
        return self

    def set_roof(self, roof: str) -> HouseBuilder:
        """Set the roof type.

        Args:
            roof: The roof type.

        Returns:
            The builder instance for method chaining.
        """
        self._house.roof = roof
        return self

    def set_windows(self, count: int) -> HouseBuilder:
        """Set the number of windows.

        Args:
            count: Number of windows.

        Returns:
            The builder instance for method chaining.
        """
        self._house.windows = count
        return self

    def set_doors(self, count: int) -> HouseBuilder:
        """Set the number of doors.

        Args:
            count: Number of doors.

        Returns:
            The builder instance for method chaining.
        """
        self._house.doors = count
        return self

    def add_garage(self) -> HouseBuilder:
        """Add a garage to the house.

        Returns:
            The builder instance for method chaining.
        """
        self._house.garage = True
        return self

    def add_garden(self) -> HouseBuilder:
        """Add a garden to the house.

        Returns:
            The builder instance for method chaining.
        """
        self._house.garden = True
        return self

    def build(self) -> House:
        """Build and return the configured House instance.

        Returns:
            The fully constructed House instance.
        """
        return self._house

    def build_simple_house(self) -> House:
        """Build a simple house with basic features.

        This is a director method that encapsulates a common configuration.

        Returns:
            A simple house.
        """
        return (
            self.set_foundation("Concrete slab")
            .set_walls("Brick")
            .set_roof("Asphalt shingles")
            .set_windows(4)
            .set_doors(1)
            .build()
        )

    def build_luxury_house(self) -> House:
        """Build a luxury house with premium features.

        This is a director method that encapsulates a premium configuration.

        Returns:
            A luxury house.
        """
        return (
            self.set_foundation("Deep foundation")
            .set_walls("Stone")
            .set_roof("Tile")
            .set_windows(12)
            .set_doors(3)
            .add_garage()
            .add_garden()
            .build()
        )
