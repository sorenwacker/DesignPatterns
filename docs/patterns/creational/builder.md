# Builder Pattern

**Category:** Creational Pattern

## Overview

Separate the construction of a complex object from its representation, allowing the same construction process to create different representations. This pattern provides a step-by-step approach to constructing objects, particularly useful when objects require many configuration parameters or complex initialization.

## Usage Guidelines

**Use when:**
- Object creation involves many steps or configuration options
- Same construction process should create different representations
- Many optional parameters would lead to multiple constructors
- Building immutable objects step by step before finalization

**Avoid when:**
- Object has few parameters and simple construction
- Object always created the same way
- Builder adds unacceptable performance overhead
- Python dataclasses or named tuples work well

## Implementation

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

### Usage

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
```

## Trade-offs

**Benefits:**
1. Readable code through fluent interface that is self-documenting
2. Step-by-step construction of complex objects incrementally
3. Same builder can create different product variants
4. Can construct immutable objects piece by piece

**Drawbacks:**
1. Adds extra classes and code, increasing complexity
2. Builder methods may duplicate product setters
3. Creates intermediate objects during construction
4. Product may be in invalid state during construction

## Real-World Examples

- SQL query builders constructing complex queries
- HTTP request builders with headers, body, parameters
- Document builders creating documents with sections
- Test data builders with various configurations

## Related Patterns

- Abstract Factory
- Composite
- Prototype
- Singleton
- Fluent Interface

## API Reference

::: design_patterns.creational.builder
    options:
      show_root_heading: true
      show_source: true
