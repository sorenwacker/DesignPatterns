# Abstract Factory Pattern

**Category:** Creational Pattern

## Intent

Provide an interface for creating families of related or dependent objects without specifying their concrete classes. The Abstract Factory pattern is particularly useful when the system needs to be independent of how its objects are created and when families of related objects must be used together.

## Problem

When creating families of related objects, direct instantiation leads to:

- Tight coupling to concrete product classes
- Difficulty switching between product families
- Inconsistency when mixing products from different families
- Violation of dependency inversion principle
- Hard-coded dependencies throughout the codebase
- Difficulty testing with mock implementations

## When to Use

Use the Abstract Factory pattern when:

- **Product families**: System needs to work with multiple families of related products
- **Family constraints**: Products from one family must be used together
- **Platform independence**: Application should be independent of product creation details
- **Interchangeable families**: You want to switch between product families easily
- **Consistent interfaces**: Different product families share common interfaces
- **Configuration-based creation**: Product family is determined by configuration

## When NOT to Use

Avoid the Abstract Factory pattern when:

- **Single product**: Only one product family exists
- **No family relationship**: Products aren't related or don't need to work together
- **Simple creation**: Product creation is straightforward
- **Overkill**: Pattern adds unnecessary complexity
- **Frequent family changes**: Adding new product families requires modifying factory interface
- **Performance critical**: Extra abstraction layer is unacceptable overhead

## Structure

The Abstract Factory pattern involves:

- **Abstract Factory**: Interface declaring methods for creating abstract products
- **Concrete Factories**: Implement abstract factory to create specific product families
- **Abstract Products**: Interfaces for each type of product
- **Concrete Products**: Implementations of abstract products for specific families
- **Client**: Uses only abstract factory and product interfaces

## Implementation

### GUI Components Example

```python
from __future__ import annotations
from abc import ABC, abstractmethod

# Abstract Products
class Button(ABC):
    """Abstract interface for buttons."""

    @abstractmethod
    def render(self) -> str:
        """Render the button."""
        pass

    @abstractmethod
    def click(self) -> str:
        """Handle button click."""
        pass

class Checkbox(ABC):
    """Abstract interface for checkboxes."""

    @abstractmethod
    def render(self) -> str:
        """Render the checkbox."""
        pass

    @abstractmethod
    def toggle(self) -> str:
        """Toggle the checkbox state."""
        pass

# Concrete Products - Windows Family
class WindowsButton(Button):
    """Concrete Windows-style button."""

    def render(self) -> str:
        return "Rendering Windows button"

    def click(self) -> str:
        return "Windows button clicked"

class WindowsCheckbox(Checkbox):
    """Concrete Windows-style checkbox."""

    def render(self) -> str:
        return "Rendering Windows checkbox"

    def toggle(self) -> str:
        return "Windows checkbox toggled"

# Concrete Products - macOS Family
class MacOSButton(Button):
    """Concrete macOS-style button."""

    def render(self) -> str:
        return "Rendering macOS button"

    def click(self) -> str:
        return "macOS button clicked"

class MacOSCheckbox(Checkbox):
    """Concrete macOS-style checkbox."""

    def render(self) -> str:
        return "Rendering macOS checkbox"

    def toggle(self) -> str:
        return "macOS checkbox toggled"

# Concrete Products - Linux Family
class LinuxButton(Button):
    """Concrete Linux-style button."""

    def render(self) -> str:
        return "Rendering Linux button"

    def click(self) -> str:
        return "Linux button clicked"

class LinuxCheckbox(Checkbox):
    """Concrete Linux-style checkbox."""

    def render(self) -> str:
        return "Rendering Linux checkbox"

    def toggle(self) -> str:
        return "Linux checkbox toggled"

# Abstract Factory
class GUIFactory(ABC):
    """Abstract factory for creating UI components."""

    @abstractmethod
    def create_button(self) -> Button:
        """Create a button."""
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        """Create a checkbox."""
        pass

# Concrete Factories
class WindowsFactory(GUIFactory):
    """Concrete factory for creating Windows UI components."""

    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()

class MacOSFactory(GUIFactory):
    """Concrete factory for creating macOS UI components."""

    def create_button(self) -> Button:
        return MacOSButton()

    def create_checkbox(self) -> Checkbox:
        return MacOSCheckbox()

class LinuxFactory(GUIFactory):
    """Concrete factory for creating Linux UI components."""

    def create_button(self) -> Button:
        return LinuxButton()

    def create_checkbox(self) -> Checkbox:
        return LinuxCheckbox()

# Client
class Application:
    """Application that uses abstract factory to create UI components."""

    def __init__(self, factory: GUIFactory) -> None:
        """Initialize application with a GUI factory."""
        self.factory = factory
        self.button = factory.create_button()
        self.checkbox = factory.create_checkbox()

    def render(self) -> str:
        """Render the application UI."""
        return f"{self.button.render()}, {self.checkbox.render()}"

    def interact(self) -> str:
        """Interact with UI components."""
        return f"{self.button.click()}, {self.checkbox.toggle()}"
```

## Usage Example

```python
# Create Windows application
windows_factory = WindowsFactory()
app = Application(windows_factory)
print(app.render())  # Rendering Windows button, Rendering Windows checkbox
print(app.interact())  # Windows button clicked, Windows checkbox toggled

# Switch to macOS by changing factory
macos_factory = MacOSFactory()
app = Application(macos_factory)
print(app.render())  # Rendering macOS button, Rendering macOS checkbox
print(app.interact())  # macOS button clicked, macOS checkbox toggled

# Switch to Linux
linux_factory = LinuxFactory()
app = Application(linux_factory)
print(app.render())  # Rendering Linux button, Rendering Linux checkbox
print(app.interact())  # Linux button clicked, Linux checkbox toggled
```

## Key Benefits

1. **Isolation**: Isolates concrete classes from client code
2. **Consistency**: Ensures products from same family are used together
3. **Easy switching**: Simple to switch between product families
4. **Open/Closed Principle**: Easy to introduce new product families
5. **Dependency Inversion**: Depends on abstractions, not concrete classes
6. **Single point of change**: Factory encapsulates product creation
7. **Testing**: Easy to substitute mock factories for testing

## Drawbacks

1. **Complexity**: Introduces many interfaces and classes
2. **Rigidity**: Adding new products requires changing all factories
3. **Learning curve**: More abstract and harder to understand
4. **Overkill**: Too complex for simple scenarios
5. **Parallel hierarchies**: Maintains parallel class hierarchies for products
6. **Factory proliferation**: Many concrete factories for each product family

## Real-World Examples

- **Cross-platform UI frameworks**: Creating platform-specific UI components (buttons, windows, dialogs)
- **Database drivers**: Creating connections, statements, and result sets for different databases
- **Document generators**: Creating different document elements for PDF, HTML, Word formats
- **Game engines**: Creating platform-specific graphics, audio, and input handlers
- **Theme systems**: Creating themed UI components with consistent styling
- **Operating system APIs**: Abstracting OS-specific system calls
- **Cloud providers**: Creating cloud-specific resources (compute, storage, networking)

## Related Patterns

- **Factory Method**: Abstract Factory uses Factory Method to create products
- **Singleton**: Concrete factories are often singletons
- **Prototype**: Can use Prototype instead of Factory Method for product creation
- **Builder**: Builder focuses on constructing complex objects, Abstract Factory on families
- **Facade**: Abstract Factory can act as facade for complex subsystems

## API Reference

::: design_patterns.creational.abstract_factory
    options:
      show_root_heading: true
      show_source: true
