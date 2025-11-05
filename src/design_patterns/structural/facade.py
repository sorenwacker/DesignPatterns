"""Facade Pattern Module

The Facade pattern provides a simplified interface to a complex subsystem. It defines
a higher-level interface that makes the subsystem easier to use by wrapping a
complicated set of objects with a single, simpler interface.

Example:
    Home theater system with many components:

    ```python
    theater = HomeTheaterFacade()

    # Simple interface hides complexity
    theater.watch_movie("Inception")
    # Internally: turns on projector, dims lights, starts audio, plays movie

    theater.end_movie()
    # Internally: stops playback, turns off equipment, raises lights
    ```
"""

from __future__ import annotations


class Projector:
    """Projector subsystem component."""

    def on(self) -> str:
        """Turn on projector.

        Returns:
            Status message.
        """
        return "Projector is on"

    def off(self) -> str:
        """Turn off projector.

        Returns:
            Status message.
        """
        return "Projector is off"

    def set_input(self, source: str) -> str:
        """Set input source.

        Args:
            source: Input source name.

        Returns:
            Status message.
        """
        return f"Projector input set to {source}"


class SoundSystem:
    """Sound system subsystem component."""

    def on(self) -> str:
        """Turn on sound system.

        Returns:
            Status message.
        """
        return "Sound system is on"

    def off(self) -> str:
        """Turn off sound system.

        Returns:
            Status message.
        """
        return "Sound system is off"

    def set_volume(self, level: int) -> str:
        """Set volume level.

        Args:
            level: Volume level (0-100).

        Returns:
            Status message.
        """
        return f"Volume set to {level}"

    def set_surround_sound(self) -> str:
        """Enable surround sound.

        Returns:
            Status message.
        """
        return "Surround sound enabled"


class DVDPlayer:
    """DVD player subsystem component."""

    def on(self) -> str:
        """Turn on DVD player.

        Returns:
            Status message.
        """
        return "DVD player is on"

    def off(self) -> str:
        """Turn off DVD player.

        Returns:
            Status message.
        """
        return "DVD player is off"

    def play(self, movie: str) -> str:
        """Play a movie.

        Args:
            movie: Movie title.

        Returns:
            Status message.
        """
        return f"Playing {movie}"

    def stop(self) -> str:
        """Stop playback.

        Returns:
            Status message.
        """
        return "DVD player stopped"


class Lights:
    """Lights subsystem component."""

    def dim(self, level: int) -> str:
        """Dim lights to level.

        Args:
            level: Light level (0-100).

        Returns:
            Status message.
        """
        return f"Lights dimmed to {level}%"

    def on(self) -> str:
        """Turn lights on.

        Returns:
            Status message.
        """
        return "Lights are on"


class HomeTheaterFacade:
    """Facade providing simplified interface to home theater subsystems."""

    def __init__(self) -> None:
        """Initialize all subsystems."""
        self.projector = Projector()
        self.sound = SoundSystem()
        self.dvd = DVDPlayer()
        self.lights = Lights()

    def watch_movie(self, movie: str) -> list[str]:
        """Set up everything to watch a movie.

        Args:
            movie: Movie title to watch.

        Returns:
            List of all operations performed.
        """
        operations = []
        operations.append(self.lights.dim(10))
        operations.append(self.projector.on())
        operations.append(self.projector.set_input("DVD"))
        operations.append(self.sound.on())
        operations.append(self.sound.set_volume(50))
        operations.append(self.sound.set_surround_sound())
        operations.append(self.dvd.on())
        operations.append(self.dvd.play(movie))
        return operations

    def end_movie(self) -> list[str]:
        """Clean up after watching a movie.

        Returns:
            List of all operations performed.
        """
        operations = []
        operations.append(self.dvd.stop())
        operations.append(self.dvd.off())
        operations.append(self.sound.off())
        operations.append(self.projector.off())
        operations.append(self.lights.on())
        return operations


class CPU:
    """CPU subsystem component."""

    def freeze(self) -> str:
        """Freeze CPU.

        Returns:
            Status message.
        """
        return "CPU frozen"

    def jump(self, position: int) -> str:
        """Jump to position.

        Args:
            position: Memory position.

        Returns:
            Status message.
        """
        return f"CPU jumped to position {position}"

    def execute(self) -> str:
        """Execute instructions.

        Returns:
            Status message.
        """
        return "CPU executing"


class Memory:
    """Memory subsystem component."""

    def load(self, position: int, data: str) -> str:
        """Load data into memory.

        Args:
            position: Memory position.
            data: Data to load.

        Returns:
            Status message.
        """
        return f"Loaded {data} at position {position}"


class HardDrive:
    """Hard drive subsystem component."""

    def read(self, sector: int, size: int) -> str:
        """Read data from hard drive.

        Args:
            sector: Disk sector.
            size: Number of bytes to read.

        Returns:
            Data read.
        """
        return f"Read {size} bytes from sector {sector}"


class ComputerFacade:
    """Facade for computer boot process."""

    def __init__(self) -> None:
        """Initialize computer subsystems."""
        self.cpu = CPU()
        self.memory = Memory()
        self.hard_drive = HardDrive()

    def start(self) -> list[str]:
        """Start the computer with a simple interface.

        Returns:
            List of boot operations.
        """
        operations = []
        operations.append(self.cpu.freeze())
        operations.append(self.memory.load(0, "boot sector"))
        operations.append(self.hard_drive.read(0, 1024))
        operations.append(self.cpu.jump(0))
        operations.append(self.cpu.execute())
        return operations
