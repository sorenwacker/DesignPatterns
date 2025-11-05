"""Bridge Pattern Module

The Bridge pattern decouples an abstraction from its implementation so that the two
can vary independently. It uses composition over inheritance to separate the interface
from the implementation, allowing both to be extended independently.

Example:
    Drawing shapes with different rendering implementations:

    ```python
    # Create a circle with vector rendering
    circle = Circle(VectorRenderer())
    circle.draw()  # Draws circle using vector graphics

    # Create a square with raster rendering
    square = Square(RasterRenderer())
    square.draw()  # Draws square using raster graphics
    ```
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Renderer(ABC):
    """Abstract implementation interface for rendering."""

    @abstractmethod
    def render_circle(self, radius: float) -> str:
        """Render a circle.

        Args:
            radius: Circle radius.

        Returns:
            Rendering result.
        """
        pass

    @abstractmethod
    def render_square(self, side: float) -> str:
        """Render a square.

        Args:
            side: Square side length.

        Returns:
            Rendering result.
        """
        pass


class VectorRenderer(Renderer):
    """Concrete implementation for vector rendering."""

    def render_circle(self, radius: float) -> str:
        """Render circle as vector.

        Args:
            radius: Circle radius.

        Returns:
            Vector rendering result.
        """
        return f"Drawing circle with radius {radius} as vector"

    def render_square(self, side: float) -> str:
        """Render square as vector.

        Args:
            side: Square side length.

        Returns:
            Vector rendering result.
        """
        return f"Drawing square with side {side} as vector"


class RasterRenderer(Renderer):
    """Concrete implementation for raster rendering."""

    def render_circle(self, radius: float) -> str:
        """Render circle as raster.

        Args:
            radius: Circle radius.

        Returns:
            Raster rendering result.
        """
        return f"Drawing circle with radius {radius} as pixels"

    def render_square(self, side: float) -> str:
        """Render square as raster.

        Args:
            side: Square side length.

        Returns:
            Raster rendering result.
        """
        return f"Drawing square with side {side} as pixels"


class Shape(ABC):
    """Abstract shape class using bridge to renderer."""

    def __init__(self, renderer: Renderer) -> None:
        """Initialize shape with a renderer.

        Args:
            renderer: The renderer implementation to use.
        """
        self.renderer = renderer

    @abstractmethod
    def draw(self) -> str:
        """Draw the shape.

        Returns:
            Drawing result.
        """
        pass

    @abstractmethod
    def resize(self, factor: float) -> None:
        """Resize the shape.

        Args:
            factor: Resize factor.
        """
        pass


class Circle(Shape):
    """Concrete circle shape."""

    def __init__(self, renderer: Renderer, radius: float = 5.0) -> None:
        """Initialize circle.

        Args:
            renderer: The renderer to use.
            radius: Circle radius.
        """
        super().__init__(renderer)
        self.radius = radius

    def draw(self) -> str:
        """Draw circle using renderer.

        Returns:
            Drawing result.
        """
        return self.renderer.render_circle(self.radius)

    def resize(self, factor: float) -> None:
        """Resize circle.

        Args:
            factor: Resize factor.
        """
        self.radius *= factor


class Square(Shape):
    """Concrete square shape."""

    def __init__(self, renderer: Renderer, side: float = 5.0) -> None:
        """Initialize square.

        Args:
            renderer: The renderer to use.
            side: Square side length.
        """
        super().__init__(renderer)
        self.side = side

    def draw(self) -> str:
        """Draw square using renderer.

        Returns:
            Drawing result.
        """
        return self.renderer.render_square(self.side)

    def resize(self, factor: float) -> None:
        """Resize square.

        Args:
            factor: Resize factor.
        """
        self.side *= factor


class Device(ABC):
    """Abstract device interface."""

    @abstractmethod
    def is_enabled(self) -> bool:
        """Check if device is enabled.

        Returns:
            True if enabled.
        """
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
        """Get current volume.

        Returns:
            Volume level.
        """
        pass

    @abstractmethod
    def set_volume(self, percent: int) -> None:
        """Set volume.

        Args:
            percent: Volume percentage.
        """
        pass


class TV(Device):
    """Concrete TV device."""

    def __init__(self) -> None:
        """Initialize TV."""
        self._enabled = False
        self._volume = 50

    def is_enabled(self) -> bool:
        """Check if TV is on.

        Returns:
            True if on.
        """
        return self._enabled

    def enable(self) -> None:
        """Turn TV on."""
        self._enabled = True

    def disable(self) -> None:
        """Turn TV off."""
        self._enabled = False

    def get_volume(self) -> int:
        """Get TV volume.

        Returns:
            Volume level.
        """
        return self._volume

    def set_volume(self, percent: int) -> None:
        """Set TV volume.

        Args:
            percent: Volume percentage.
        """
        self._volume = max(0, min(100, percent))


class Radio(Device):
    """Concrete radio device."""

    def __init__(self) -> None:
        """Initialize radio."""
        self._enabled = False
        self._volume = 30

    def is_enabled(self) -> bool:
        """Check if radio is on.

        Returns:
            True if on.
        """
        return self._enabled

    def enable(self) -> None:
        """Turn radio on."""
        self._enabled = True

    def disable(self) -> None:
        """Turn radio off."""
        self._enabled = False

    def get_volume(self) -> int:
        """Get radio volume.

        Returns:
            Volume level.
        """
        return self._volume

    def set_volume(self, percent: int) -> None:
        """Set radio volume.

        Args:
            percent: Volume percentage.
        """
        self._volume = max(0, min(100, percent))


class RemoteControl:
    """Abstraction for remote control using bridge to device."""

    def __init__(self, device: Device) -> None:
        """Initialize remote with a device.

        Args:
            device: The device to control.
        """
        self.device = device

    def toggle_power(self) -> str:
        """Toggle device power.

        Returns:
            Status message.
        """
        if self.device.is_enabled():
            self.device.disable()
            return "Device turned off"
        else:
            self.device.enable()
            return "Device turned on"

    def volume_up(self) -> str:
        """Increase volume.

        Returns:
            Status message.
        """
        current = self.device.get_volume()
        self.device.set_volume(current + 10)
        return f"Volume increased to {self.device.get_volume()}"

    def volume_down(self) -> str:
        """Decrease volume.

        Returns:
            Status message.
        """
        current = self.device.get_volume()
        self.device.set_volume(current - 10)
        return f"Volume decreased to {self.device.get_volume()}"


class AdvancedRemoteControl(RemoteControl):
    """Extended remote control with additional features."""

    def mute(self) -> str:
        """Mute the device.

        Returns:
            Status message.
        """
        self.device.set_volume(0)
        return "Device muted"
