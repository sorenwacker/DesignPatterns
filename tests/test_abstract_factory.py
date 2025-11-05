"""Tests for the Abstract Factory pattern."""

from design_patterns.creational.abstract_factory import (
    Application,
    LinuxFactory,
    MacOSFactory,
    WindowsFactory,
)


def test_windows_button():
    """Test Windows button creation and behavior."""
    factory = WindowsFactory()
    button = factory.create_button()

    assert button.render() == "Rendering Windows button"
    assert button.click() == "Windows button clicked"


def test_windows_checkbox():
    """Test Windows checkbox creation and behavior."""
    factory = WindowsFactory()
    checkbox = factory.create_checkbox()

    assert checkbox.render() == "Rendering Windows checkbox"
    assert checkbox.toggle() == "Windows checkbox toggled"


def test_macos_button():
    """Test macOS button creation and behavior."""
    factory = MacOSFactory()
    button = factory.create_button()

    assert button.render() == "Rendering macOS button"
    assert button.click() == "macOS button clicked"


def test_macos_checkbox():
    """Test macOS checkbox creation and behavior."""
    factory = MacOSFactory()
    checkbox = factory.create_checkbox()

    assert checkbox.render() == "Rendering macOS checkbox"
    assert checkbox.toggle() == "macOS checkbox toggled"


def test_linux_button():
    """Test Linux button creation and behavior."""
    factory = LinuxFactory()
    button = factory.create_button()

    assert button.render() == "Rendering Linux button"
    assert button.click() == "Linux button clicked"


def test_linux_checkbox():
    """Test Linux checkbox creation and behavior."""
    factory = LinuxFactory()
    checkbox = factory.create_checkbox()

    assert checkbox.render() == "Rendering Linux checkbox"
    assert checkbox.toggle() == "Linux checkbox toggled"


def test_windows_application():
    """Test application with Windows factory."""
    app = Application(WindowsFactory())

    assert "Windows button" in app.render()
    assert "Windows checkbox" in app.render()
    assert "Windows button clicked" in app.interact()
    assert "Windows checkbox toggled" in app.interact()


def test_macos_application():
    """Test application with macOS factory."""
    app = Application(MacOSFactory())

    assert "macOS button" in app.render()
    assert "macOS checkbox" in app.render()
    assert "macOS button clicked" in app.interact()
    assert "macOS checkbox toggled" in app.interact()


def test_linux_application():
    """Test application with Linux factory."""
    app = Application(LinuxFactory())

    assert "Linux button" in app.render()
    assert "Linux checkbox" in app.render()
    assert "Linux button clicked" in app.interact()
    assert "Linux checkbox toggled" in app.interact()


def test_factory_interchangeability():
    """Test that factories are interchangeable."""
    factories = [WindowsFactory(), MacOSFactory(), LinuxFactory()]

    for factory in factories:
        app = Application(factory)
        assert "button" in app.render().lower()
        assert "checkbox" in app.render().lower()
