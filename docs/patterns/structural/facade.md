# Facade Pattern

**Category:** Structural Pattern

## Intent

Provide a simplified interface to a complex subsystem. The Facade pattern defines a higher-level interface that makes the subsystem easier to use by wrapping a complicated set of objects with a single, simpler interface.

## Problem

When working with complex subsystems, direct interaction leads to:

- Clients tightly coupled to many subsystem classes
- Complex initialization and configuration
- Difficult to understand subsystem interactions
- Hard to change subsystem without affecting clients
- Steep learning curve for subsystem usage

## When to Use

Use the Facade pattern when:

- **Complex subsystem**: Subsystem has many classes and complex interactions
- **Simplify interface**: Want to provide simple interface to complex functionality
- **Layer subsystems**: Creating layers in application architecture
- **Decouple clients**: Want to decouple clients from subsystem
- **Common usage**: Most clients need only subset of subsystem functionality
- **Entry point**: Need single entry point to subsystem

## When NOT to Use

Avoid the Facade pattern when:

- **Simple subsystem**: Subsystem is already simple
- **Full access needed**: Clients need fine-grained control
- **No common interface**: No common usage patterns exist
- **Unnecessary abstraction**: Adds complexity without benefit
- **Performance**: Facade overhead is unacceptable

## Structure

The Facade pattern involves:

- **Facade**: Provides simplified interface to subsystem
- **Subsystem Classes**: Implement subsystem functionality
- **Client**: Uses facade instead of subsystem classes directly

## Implementation

### Home Theater Example

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

### Computer Facade Example

```python
class CPU:
    """CPU subsystem component."""

    def freeze(self) -> str:
        """Freeze CPU."""
        return "CPU frozen"

    def jump(self, position: int) -> str:
        """Jump to position."""
        return f"CPU jumped to position {position}"

    def execute(self) -> str:
        """Execute instructions."""
        return "CPU executing"

class Memory:
    """Memory subsystem component."""

    def load(self, position: int, data: str) -> str:
        """Load data into memory."""
        return f"Loaded {data} at position {position}"

class HardDrive:
    """Hard drive subsystem component."""

    def read(self, sector: int, size: int) -> str:
        """Read data from hard drive."""
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
```

## Usage Example

```python
# Without facade - complex setup
projector = Projector()
sound = SoundSystem()
dvd = DVDPlayer()
lights = Lights()

lights.dim(10)
projector.on()
projector.set_input("DVD")
sound.on()
sound.set_volume(50)
sound.set_surround_sound()
dvd.on()
dvd.play("Inception")
# ... many steps

# With facade - simple interface
theater = HomeTheaterFacade()
operations = theater.watch_movie("Inception")
# All complexity hidden behind simple method

# Later, end movie with one call
operations = theater.end_movie()

# Computer boot example
computer = ComputerFacade()
boot_steps = computer.start()
print("\n".join(boot_steps))
```

## Key Benefits

1. **Simplified interface**: Provides simple interface to complex subsystem
2. **Reduced coupling**: Clients decoupled from subsystem classes
3. **Layered architecture**: Supports layering in application
4. **Easier to use**: Subsystem becomes easier to use
5. **Flexibility**: Can still access subsystem classes directly if needed
6. **Maintainability**: Changes to subsystem don't affect clients

## Drawbacks

1. **God object**: Facade can become too large and complex
2. **Limited functionality**: May not expose all subsystem features
3. **Tight coupling**: Facade tightly coupled to subsystem
4. **Additional layer**: Adds another layer of abstraction
5. **Inflexibility**: May not suit all client needs

## Real-World Examples

- **Framework APIs**: Simplified APIs for complex frameworks
- **Database libraries**: High-level query builders hiding SQL complexity
- **Compiler frontends**: Simple interface to complex compilation process
- **Network libraries**: Simple HTTP client hiding socket complexity
- **Graphics libraries**: Simple drawing API hiding rendering complexity
- **Operating system APIs**: High-level APIs for system calls
- **Cloud SDKs**: Simplified interfaces to cloud services

## Related Patterns

- **Abstract Factory**: Can use Facade to create subsystem objects
- **Mediator**: Similar to Facade but bidirectional communication
- **Singleton**: Facade is often implemented as singleton
- **Adapter**: Adapter changes interface, Facade simplifies it

## API Reference

::: design_patterns.structural.facade
    options:
      show_root_heading: true
      show_source: true
