# Abstract Factory Pattern

**Category:** Creational Pattern

## Overview

Provide an interface for creating families of related or dependent objects without specifying their concrete classes. This pattern is useful when the system needs to be independent of how its objects are created and when families of related objects must be used together to ensure consistency.

## Usage Guidelines

**Use when:**
- System needs to work with multiple families of related products
- Products from one family must be used together for consistency
- You want to switch between product families easily
- Application should be independent of product creation details

**Avoid when:**
- Only one product family exists
- Products aren't related or don't need to work together
- Product creation is straightforward
- Adding new product families requires modifying the factory interface

## Implementation

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

### Usage

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
```

## Trade-offs

**Benefits:**
1. Isolates concrete classes from client code
2. Ensures products from same family are used together
3. Easy to switch between product families
4. Easy to introduce new product families (Open/Closed Principle)

**Drawbacks:**
1. Introduces many interfaces and classes, increasing complexity
2. Adding new products requires changing all factories
3. More abstract and harder to understand than simpler patterns
4. Maintains parallel class hierarchies for products

## Real-World Examples

- Cross-platform UI frameworks creating platform-specific components
- Database drivers for different databases
- Document generators for PDF, HTML, Word formats
- Theme systems with consistent styled components

## Related Patterns

- Factory Method
- Singleton
- Prototype
- Builder
- Facade

## API Reference

::: design_patterns.creational.abstract_factory
    options:
      show_root_heading: true
      show_source: true
