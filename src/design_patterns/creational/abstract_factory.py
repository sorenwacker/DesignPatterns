"""Abstract Factory Pattern Module

The Abstract Factory pattern provides an interface for creating families of related
or dependent objects without specifying their concrete classes. This pattern is
particularly useful when the system needs to be independent of how its objects are
created and when families of related objects must be used together.

Example:
    Creating UI components for different platforms:

    ```python
    # Create a Windows UI factory
    factory = WindowsFactory()
    button = factory.create_button()
    checkbox = factory.create_checkbox()

    button.render()  # Renders Windows-style button
    checkbox.render()  # Renders Windows-style checkbox

    # Switch to macOS UI factory
    factory = MacOSFactory()
    button = factory.create_button()
    checkbox = factory.create_checkbox()

    button.render()  # Renders macOS-style button
    checkbox.render()  # Renders macOS-style checkbox
    ```
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Button(ABC):
    """Abstract interface for buttons."""

    @abstractmethod
    def render(self) -> str:
        """Render the button.

        Returns:
            String representation of the rendered button.
        """
        pass

    @abstractmethod
    def click(self) -> str:
        """Handle button click.

        Returns:
            String describing the click action.
        """
        pass


class Checkbox(ABC):
    """Abstract interface for checkboxes."""

    @abstractmethod
    def render(self) -> str:
        """Render the checkbox.

        Returns:
            String representation of the rendered checkbox.
        """
        pass

    @abstractmethod
    def toggle(self) -> str:
        """Toggle the checkbox state.

        Returns:
            String describing the toggle action.
        """
        pass


class WindowsButton(Button):
    """Concrete Windows-style button."""

    def render(self) -> str:
        """Render Windows button.

        Returns:
            Windows button rendering.
        """
        return "Rendering Windows button"

    def click(self) -> str:
        """Handle Windows button click.

        Returns:
            Windows click action.
        """
        return "Windows button clicked"


class WindowsCheckbox(Checkbox):
    """Concrete Windows-style checkbox."""

    def render(self) -> str:
        """Render Windows checkbox.

        Returns:
            Windows checkbox rendering.
        """
        return "Rendering Windows checkbox"

    def toggle(self) -> str:
        """Toggle Windows checkbox.

        Returns:
            Windows toggle action.
        """
        return "Windows checkbox toggled"


class MacOSButton(Button):
    """Concrete macOS-style button."""

    def render(self) -> str:
        """Render macOS button.

        Returns:
            macOS button rendering.
        """
        return "Rendering macOS button"

    def click(self) -> str:
        """Handle macOS button click.

        Returns:
            macOS click action.
        """
        return "macOS button clicked"


class MacOSCheckbox(Checkbox):
    """Concrete macOS-style checkbox."""

    def render(self) -> str:
        """Render macOS checkbox.

        Returns:
            macOS checkbox rendering.
        """
        return "Rendering macOS checkbox"

    def toggle(self) -> str:
        """Toggle macOS checkbox.

        Returns:
            macOS toggle action.
        """
        return "macOS checkbox toggled"


class LinuxButton(Button):
    """Concrete Linux-style button."""

    def render(self) -> str:
        """Render Linux button.

        Returns:
            Linux button rendering.
        """
        return "Rendering Linux button"

    def click(self) -> str:
        """Handle Linux button click.

        Returns:
            Linux click action.
        """
        return "Linux button clicked"


class LinuxCheckbox(Checkbox):
    """Concrete Linux-style checkbox."""

    def render(self) -> str:
        """Render Linux checkbox.

        Returns:
            Linux checkbox rendering.
        """
        return "Rendering Linux checkbox"

    def toggle(self) -> str:
        """Toggle Linux checkbox.

        Returns:
            Linux toggle action.
        """
        return "Linux checkbox toggled"


class GUIFactory(ABC):
    """Abstract factory for creating UI components."""

    @abstractmethod
    def create_button(self) -> Button:
        """Create a button.

        Returns:
            A button instance.
        """
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        """Create a checkbox.

        Returns:
            A checkbox instance.
        """
        pass


class WindowsFactory(GUIFactory):
    """Concrete factory for creating Windows UI components."""

    def create_button(self) -> Button:
        """Create a Windows button.

        Returns:
            WindowsButton instance.
        """
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        """Create a Windows checkbox.

        Returns:
            WindowsCheckbox instance.
        """
        return WindowsCheckbox()


class MacOSFactory(GUIFactory):
    """Concrete factory for creating macOS UI components."""

    def create_button(self) -> Button:
        """Create a macOS button.

        Returns:
            MacOSButton instance.
        """
        return MacOSButton()

    def create_checkbox(self) -> Checkbox:
        """Create a macOS checkbox.

        Returns:
            MacOSCheckbox instance.
        """
        return MacOSCheckbox()


class LinuxFactory(GUIFactory):
    """Concrete factory for creating Linux UI components."""

    def create_button(self) -> Button:
        """Create a Linux button.

        Returns:
            LinuxButton instance.
        """
        return LinuxButton()

    def create_checkbox(self) -> Checkbox:
        """Create a Linux checkbox.

        Returns:
            LinuxCheckbox instance.
        """
        return LinuxCheckbox()


class Application:
    """Application that uses abstract factory to create UI components."""

    def __init__(self, factory: GUIFactory) -> None:
        """Initialize application with a GUI factory.

        Args:
            factory: The GUI factory to use for creating components.
        """
        self.factory = factory
        self.button = factory.create_button()
        self.checkbox = factory.create_checkbox()

    def render(self) -> str:
        """Render the application UI.

        Returns:
            Combined rendering of all UI components.
        """
        return f"{self.button.render()}, {self.checkbox.render()}"

    def interact(self) -> str:
        """Interact with UI components.

        Returns:
            Combined interaction results.
        """
        return f"{self.button.click()}, {self.checkbox.toggle()}"
