# Bridge Pattern

**Category:** Structural Pattern

## Intent

Decouple an abstraction from its implementation so that the two can vary independently. The Bridge pattern uses composition over inheritance to separate the interface from the implementation, allowing both to be extended independently without affecting each other.

## Problem

When abstractions and implementations are tightly coupled through inheritance, it leads to:

- Exponential growth of subclasses for each combination
- Difficulty adding new abstractions or implementations
- Tight binding between abstraction and implementation
- Changes in implementation affecting abstraction
- Inability to switch implementations at runtime

## When to Use

Use the Bridge pattern when:

- **Avoid permanent binding**: Want to avoid permanent binding between abstraction and implementation
- **Independent extension**: Both abstraction and implementation should be extended independently
- **Runtime switching**: Need to switch implementations at runtime
- **Multiple implementations**: Multiple implementations of abstraction exist
- **Platform independence**: Implementing platform-independent interfaces
- **Hide implementation**: Want to hide implementation details from clients

## When NOT to Use

Avoid the Bridge pattern when:

- **Single implementation**: Only one implementation exists
- **No variation**: Implementation doesn't vary
- **Simple inheritance**: Simple inheritance suffices
- **Overkill**: Pattern adds unnecessary complexity
- **Performance critical**: Extra indirection is unacceptable

## Structure

The Bridge pattern involves:

- **Abstraction**: Defines abstraction interface and maintains reference to implementation
- **Refined Abstraction**: Extends abstraction interface
- **Implementation**: Defines implementation interface
- **Concrete Implementation**: Implements the implementation interface

## Implementation

### Shape Rendering Example

```python
from __future__ import annotations
from abc import ABC, abstractmethod

# Implementation Interface
class Renderer(ABC):
    """Abstract implementation interface for rendering."""

    @abstractmethod
    def render_circle(self, radius: float) -> str:
        """Render a circle."""
        pass

    @abstractmethod
    def render_square(self, side: float) -> str:
        """Render a square."""
        pass

# Concrete Implementations
class VectorRenderer(Renderer):
    """Concrete implementation for vector rendering."""

    def render_circle(self, radius: float) -> str:
        """Render circle as vector."""
        return f"Drawing circle with radius {radius} as vector"

    def render_square(self, side: float) -> str:
        """Render square as vector."""
        return f"Drawing square with side {side} as vector"

class RasterRenderer(Renderer):
    """Concrete implementation for raster rendering."""

    def render_circle(self, radius: float) -> str:
        """Render circle as raster."""
        return f"Drawing circle with radius {radius} as pixels"

    def render_square(self, side: float) -> str:
        """Render square as raster."""
        return f"Drawing square with side {side} as pixels"

# Abstraction
class Shape(ABC):
    """Abstract shape class using bridge to renderer."""

    def __init__(self, renderer: Renderer) -> None:
        """Initialize shape with a renderer."""
        self.renderer = renderer

    @abstractmethod
    def draw(self) -> str:
        """Draw the shape."""
        pass

    @abstractmethod
    def resize(self, factor: float) -> None:
        """Resize the shape."""
        pass

# Refined Abstractions
class Circle(Shape):
    """Concrete circle shape."""

    def __init__(self, renderer: Renderer, radius: float = 5.0) -> None:
        """Initialize circle."""
        super().__init__(renderer)
        self.radius = radius

    def draw(self) -> str:
        """Draw circle using renderer."""
        return self.renderer.render_circle(self.radius)

    def resize(self, factor: float) -> None:
        """Resize circle."""
        self.radius *= factor

class Square(Shape):
    """Concrete square shape."""

    def __init__(self, renderer: Renderer, side: float = 5.0) -> None:
        """Initialize square."""
        super().__init__(renderer)
        self.side = side

    def draw(self) -> str:
        """Draw square using renderer."""
        return self.renderer.render_square(self.side)

    def resize(self, factor: float) -> None:
        """Resize square."""
        self.side *= factor
```

### Remote Control Example

```python
class Device(ABC):
    """Abstract device interface."""

    @abstractmethod
    def is_enabled(self) -> bool:
        """Check if device is enabled."""
        pass

    @abstractmethod
    def enable(self) -> None:
        """Enable the device."""
        pass

    @abstractmethod
    def disable(self) -> None:
        """Disable the device."""
        pass

    @abstractmethod
    def get_volume(self) -> int:
        """Get current volume."""
        pass

    @abstractmethod
    def set_volume(self, percent: int) -> None:
        """Set volume."""
        pass

class TV(Device):
    """Concrete TV device."""

    def __init__(self) -> None:
        """Initialize TV."""
        self._enabled = False
        self._volume = 50

    def is_enabled(self) -> bool:
        """Check if TV is on."""
        return self._enabled

    def enable(self) -> None:
        """Turn TV on."""
        self._enabled = True

    def disable(self) -> None:
        """Turn TV off."""
        self._enabled = False

    def get_volume(self) -> int:
        """Get TV volume."""
        return self._volume

    def set_volume(self, percent: int) -> None:
        """Set TV volume."""
        self._volume = max(0, min(100, percent))

class Radio(Device):
    """Concrete radio device."""

    def __init__(self) -> None:
        """Initialize radio."""
        self._enabled = False
        self._volume = 30

    def is_enabled(self) -> bool:
        """Check if radio is on."""
        return self._enabled

    def enable(self) -> None:
        """Turn radio on."""
        self._enabled = True

    def disable(self) -> None:
        """Turn radio off."""
        self._enabled = False

    def get_volume(self) -> int:
        """Get radio volume."""
        return self._volume

    def set_volume(self, percent: int) -> None:
        """Set radio volume."""
        self._volume = max(0, min(100, percent))

class RemoteControl:
    """Abstraction for remote control using bridge to device."""

    def __init__(self, device: Device) -> None:
        """Initialize remote with a device."""
        self.device = device

    def toggle_power(self) -> str:
        """Toggle device power."""
        if self.device.is_enabled():
            self.device.disable()
            return "Device turned off"
        else:
            self.device.enable()
            return "Device turned on"

    def volume_up(self) -> str:
        """Increase volume."""
        current = self.device.get_volume()
        self.device.set_volume(current + 10)
        return f"Volume increased to {self.device.get_volume()}"

    def volume_down(self) -> str:
        """Decrease volume."""
        current = self.device.get_volume()
        self.device.set_volume(current - 10)
        return f"Volume decreased to {self.device.get_volume()}"

class AdvancedRemoteControl(RemoteControl):
    """Extended remote control with additional features."""

    def mute(self) -> str:
        """Mute the device."""
        self.device.set_volume(0)
        return "Device muted"
```

## Usage Example

```python
# Create shapes with different renderers
circle_vector = Circle(VectorRenderer(), 5.0)
print(circle_vector.draw())  # Drawing circle with radius 5.0 as vector

circle_raster = Circle(RasterRenderer(), 5.0)
print(circle_raster.draw())  # Drawing circle with radius 5.0 as pixels

square_vector = Square(VectorRenderer(), 10.0)
print(square_vector.draw())  # Drawing square with side 10.0 as vector

# Resize and redraw
circle_vector.resize(2.0)
print(circle_vector.draw())  # Drawing circle with radius 10.0 as vector

# Remote control with different devices
tv = TV()
tv_remote = RemoteControl(tv)
print(tv_remote.toggle_power())  # Device turned on
print(tv_remote.volume_up())  # Volume increased to 60

radio = Radio()
radio_remote = AdvancedRemoteControl(radio)
print(radio_remote.toggle_power())  # Device turned on
print(radio_remote.mute())  # Device muted
```

## Key Benefits

1. **Independent extension**: Abstraction and implementation can vary independently
2. **Runtime binding**: Implementation can be selected or switched at runtime
3. **Platform independence**: Isolates platform-specific code
4. **Hide implementation**: Implementation details hidden from clients
5. **Open/Closed Principle**: New abstractions and implementations without changing existing code
6. **Composition over inheritance**: Uses composition instead of inheritance

## Drawbacks

1. **Complexity**: Adds complexity with additional abstractions
2. **Indirection**: Extra layer of indirection
3. **Design difficulty**: Can be hard to design proper abstraction/implementation split
4. **Overkill**: Too complex for simple scenarios

## Real-World Examples

- **GUI frameworks**: Separating GUI from platform-specific rendering
- **Database drivers**: Abstract database operations from specific database implementations
- **Graphics systems**: Separating shapes from rendering methods
- **Device drivers**: Separating device operations from hardware implementations
- **Messaging systems**: Separating message format from delivery mechanism
- **Persistence layers**: Separating domain objects from storage mechanisms

## Related Patterns

- **Abstract Factory**: Can create and configure bridges
- **Adapter**: Changes interface, Bridge separates abstraction from implementation
- **State**: Bridge structure can be used for state pattern

## API Reference

::: design_patterns.structural.bridge
    options:
      show_root_heading: true
      show_source: true
