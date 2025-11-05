"""Tests for the Facade pattern."""

from design_patterns.structural.facade import ComputerFacade, HomeTheaterFacade


def test_home_theater_watch_movie():
    """Test watching a movie through facade."""
    theater = HomeTheaterFacade()
    operations = theater.watch_movie("Inception")

    assert len(operations) == 8
    assert any("dimmed" in op for op in operations)
    assert any("Projector is on" in op for op in operations)
    assert any("Sound system is on" in op for op in operations)
    assert any("Playing Inception" in op for op in operations)


def test_home_theater_end_movie():
    """Test ending movie through facade."""
    theater = HomeTheaterFacade()
    operations = theater.end_movie()

    assert len(operations) == 5
    assert any("stopped" in op for op in operations)
    assert any("Projector is off" in op for op in operations)
    assert any("Sound system is off" in op for op in operations)
    assert any("Lights are on" in op for op in operations)


def test_home_theater_complete_workflow():
    """Test complete movie watching workflow."""
    theater = HomeTheaterFacade()

    start_ops = theater.watch_movie("The Matrix")
    assert any("Matrix" in op for op in start_ops)

    end_ops = theater.end_movie()
    assert any("stopped" in op for op in end_ops)


def test_projector_operations():
    """Test projector can be used independently."""
    theater = HomeTheaterFacade()

    result = theater.projector.on()
    assert result == "Projector is on"

    result = theater.projector.set_input("HDMI")
    assert result == "Projector input set to HDMI"

    result = theater.projector.off()
    assert result == "Projector is off"


def test_sound_system_operations():
    """Test sound system can be used independently."""
    theater = HomeTheaterFacade()

    result = theater.sound.on()
    assert result == "Sound system is on"

    result = theater.sound.set_volume(75)
    assert result == "Volume set to 75"

    result = theater.sound.set_surround_sound()
    assert result == "Surround sound enabled"


def test_dvd_player_operations():
    """Test DVD player can be used independently."""
    theater = HomeTheaterFacade()

    result = theater.dvd.on()
    assert result == "DVD player is on"

    result = theater.dvd.play("Avatar")
    assert result == "Playing Avatar"

    result = theater.dvd.stop()
    assert result == "DVD player stopped"


def test_lights_operations():
    """Test lights can be used independently."""
    theater = HomeTheaterFacade()

    result = theater.lights.dim(25)
    assert result == "Lights dimmed to 25%"

    result = theater.lights.on()
    assert result == "Lights are on"


def test_computer_start():
    """Test computer boot through facade."""
    computer = ComputerFacade()
    operations = computer.start()

    assert len(operations) == 5
    assert any("frozen" in op for op in operations)
    assert any("boot sector" in op for op in operations)
    assert any("Read" in op for op in operations)
    assert any("jumped" in op for op in operations)
    assert any("executing" in op for op in operations)


def test_computer_boot_sequence():
    """Test computer boot operations are in correct order."""
    computer = ComputerFacade()
    operations = computer.start()

    assert "frozen" in operations[0]
    assert "boot sector" in operations[1]
    assert "Read" in operations[2]
    assert "jumped" in operations[3]
    assert "executing" in operations[4]


def test_computer_subsystems_accessible():
    """Test that subsystems can be accessed directly."""
    computer = ComputerFacade()

    cpu_result = computer.cpu.freeze()
    assert cpu_result == "CPU frozen"

    mem_result = computer.memory.load(100, "test data")
    assert "test data" in mem_result

    hd_result = computer.hard_drive.read(5, 512)
    assert "512 bytes" in hd_result
    assert "sector 5" in hd_result


def test_facade_simplifies_interface():
    """Test that facade provides simpler interface than using subsystems directly."""
    theater = HomeTheaterFacade()

    # With facade: one method call
    operations = theater.watch_movie("Test Movie")
    assert len(operations) == 8

    # Without facade: would need 8 method calls
    # This demonstrates the simplification provided by the facade
