"""Tests for the Bridge pattern."""

from design_patterns.structural.bridge import (
    AdvancedRemoteControl,
    Circle,
    Radio,
    RasterRenderer,
    RemoteControl,
    Square,
    TV,
    VectorRenderer,
)


def test_circle_with_vector_renderer():
    """Test circle with vector rendering."""
    circle = Circle(VectorRenderer(), radius=10.0)
    result = circle.draw()

    assert "circle" in result
    assert "10" in result
    assert "vector" in result


def test_circle_with_raster_renderer():
    """Test circle with raster rendering."""
    circle = Circle(RasterRenderer(), radius=10.0)
    result = circle.draw()

    assert "circle" in result
    assert "10" in result
    assert "pixels" in result


def test_square_with_vector_renderer():
    """Test square with vector rendering."""
    square = Square(VectorRenderer(), side=8.0)
    result = square.draw()

    assert "square" in result
    assert "8" in result
    assert "vector" in result


def test_square_with_raster_renderer():
    """Test square with raster rendering."""
    square = Square(RasterRenderer(), side=8.0)
    result = square.draw()

    assert "square" in result
    assert "8" in result
    assert "pixels" in result


def test_circle_resize():
    """Test circle resizing."""
    circle = Circle(VectorRenderer(), radius=10.0)
    circle.resize(2.0)

    assert circle.radius == 20.0


def test_square_resize():
    """Test square resizing."""
    square = Square(RasterRenderer(), side=5.0)
    square.resize(3.0)

    assert square.side == 15.0


def test_shape_renderer_independence():
    """Test that shapes and renderers are independent."""
    vector = VectorRenderer()
    raster = RasterRenderer()

    circle1 = Circle(vector, 5.0)
    circle2 = Circle(raster, 5.0)

    result1 = circle1.draw()
    result2 = circle2.draw()

    assert "vector" in result1
    assert "pixels" in result2


def test_tv_device():
    """Test TV device functionality."""
    tv = TV()

    assert tv.is_enabled() is False

    tv.enable()
    assert tv.is_enabled() is True

    tv.set_volume(75)
    assert tv.get_volume() == 75

    tv.disable()
    assert tv.is_enabled() is False


def test_radio_device():
    """Test radio device functionality."""
    radio = Radio()

    assert radio.is_enabled() is False
    assert radio.get_volume() == 30

    radio.enable()
    radio.set_volume(60)
    assert radio.get_volume() == 60


def test_remote_control_with_tv():
    """Test remote control with TV."""
    tv = TV()
    remote = RemoteControl(tv)

    result = remote.toggle_power()
    assert "turned on" in result
    assert tv.is_enabled() is True

    result = remote.toggle_power()
    assert "turned off" in result
    assert tv.is_enabled() is False


def test_remote_control_with_radio():
    """Test remote control with radio."""
    radio = Radio()
    remote = RemoteControl(radio)

    remote.toggle_power()
    assert radio.is_enabled() is True


def test_remote_volume_up():
    """Test remote volume up."""
    tv = TV()
    remote = RemoteControl(tv)

    initial_volume = tv.get_volume()
    result = remote.volume_up()

    assert tv.get_volume() == initial_volume + 10
    assert str(tv.get_volume()) in result


def test_remote_volume_down():
    """Test remote volume down."""
    tv = TV()
    remote = RemoteControl(tv)

    initial_volume = tv.get_volume()
    result = remote.volume_down()

    assert tv.get_volume() == initial_volume - 10
    assert str(tv.get_volume()) in result


def test_volume_bounds():
    """Test that volume is bounded between 0 and 100."""
    tv = TV()
    tv.set_volume(150)
    assert tv.get_volume() == 100

    tv.set_volume(-10)
    assert tv.get_volume() == 0


def test_advanced_remote_mute():
    """Test advanced remote mute functionality."""
    tv = TV()
    remote = AdvancedRemoteControl(tv)

    tv.set_volume(75)
    result = remote.mute()

    assert tv.get_volume() == 0
    assert "muted" in result


def test_advanced_remote_inherits_basic_functions():
    """Test that advanced remote has basic functions."""
    radio = Radio()
    remote = AdvancedRemoteControl(radio)

    remote.toggle_power()
    assert radio.is_enabled() is True

    remote.volume_up()
    assert radio.get_volume() > 30


def test_bridge_allows_independent_extension():
    """Test that abstraction and implementation can vary independently."""
    # Can use any device with any remote
    remotes = [RemoteControl, AdvancedRemoteControl]

    for remote_class in remotes:
        tv = TV()
        radio = Radio()

        tv_remote = remote_class(tv)
        radio_remote = remote_class(radio)

        tv_result = tv_remote.toggle_power()
        radio_result = radio_remote.toggle_power()

        assert "turned on" in tv_result
        assert "turned on" in radio_result
