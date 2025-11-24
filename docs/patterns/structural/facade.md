# Facade Pattern

**Category:** Structural Pattern

## Overview

Provide a simplified interface to a complex subsystem. This pattern defines a higher-level interface that makes the subsystem easier to use by wrapping a complicated set of objects with a single, simpler interface.

## Usage Guidelines

**Use when:**

- Subsystem has many classes and complex interactions
- Want to provide simple interface to complex functionality
- Creating layers in application architecture
- Most clients need only subset of subsystem functionality

**Avoid when:**

- Subsystem is already simple
- Clients need fine-grained control
- No common usage patterns exist
- Facade overhead is unacceptable for performance

## Implementation

```python
from __future__ import annotations

# Subsystem Classes
class Projector:
    """Projector subsystem component."""

    def on(self) -> str:
        """Turn on projector."""
        return "Projector is on"

    def off(self) -> str:
        """Turn off projector."""
        return "Projector is off"

    def set_input(self, source: str) -> str:
        """Set input source."""
        return f"Projector input set to {source}"

class SoundSystem:
    """Sound system subsystem component."""

    def on(self) -> str:
        """Turn on sound system."""
        return "Sound system is on"

    def off(self) -> str:
        """Turn off sound system."""
        return "Sound system is off"

    def set_volume(self, level: int) -> str:
        """Set volume level."""
        return f"Volume set to {level}"

    def set_surround_sound(self) -> str:
        """Enable surround sound."""
        return "Surround sound enabled"

class DVDPlayer:
    """DVD player subsystem component."""

    def on(self) -> str:
        """Turn on DVD player."""
        return "DVD player is on"

    def off(self) -> str:
        """Turn off DVD player."""
        return "DVD player is off"

    def play(self, movie: str) -> str:
        """Play a movie."""
        return f"Playing {movie}"

    def stop(self) -> str:
        """Stop playback."""
        return "DVD player stopped"

class Lights:
    """Lights subsystem component."""

    def dim(self, level: int) -> str:
        """Dim lights to level."""
        return f"Lights dimmed to {level}%"

    def on(self) -> str:
        """Turn lights on."""
        return "Lights are on"

# Facade
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
```

### Usage

```python
# With facade - simple interface
theater = HomeTheaterFacade()
operations = theater.watch_movie("Inception")
# All complexity hidden behind simple method

# Later, end movie with one call
operations = theater.end_movie()
```

## Trade-offs

**Benefits:**

1. Provides simple interface to complex subsystem
2. Clients decoupled from subsystem classes reducing coupling
3. Supports layering in application architecture
4. Subsystem becomes easier to use

**Drawbacks:**

1. Facade can become too large and complex (God object)
2. May not expose all subsystem features limiting functionality
3. Facade tightly coupled to subsystem
4. Adds another layer of abstraction

## Real-World Examples

- Framework APIs providing simplified interfaces
- Database libraries with high-level query builders hiding SQL complexity
- Network libraries with simple HTTP client hiding socket complexity
- Cloud SDKs with simplified interfaces to cloud services

## Related Patterns

- Abstract Factory
- Mediator
- Singleton
- Adapter

## API Reference

::: design_patterns.structural.facade
    options:
      show_root_heading: true
      show_source: true
