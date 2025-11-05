"""Tests for the Builder pattern."""

from design_patterns.creational.builder import ComputerBuilder, HouseBuilder


def test_computer_builder_basic():
    """Test building a basic computer."""
    builder = ComputerBuilder()
    computer = builder.set_cpu("Intel i5").set_ram(16).build()

    assert computer.cpu == "Intel i5"
    assert computer.ram == 16
    assert computer.gpu is None


def test_computer_builder_full():
    """Test building a fully configured computer."""
    builder = ComputerBuilder()
    computer = (builder
                .set_cpu("Intel i9")
                .set_ram(32)
                .set_storage("1TB SSD")
                .set_gpu("NVIDIA RTX 4090")
                .set_os("Ubuntu Linux")
                .add_peripheral("Mechanical Keyboard")
                .add_peripheral("Gaming Mouse")
                .build())

    assert computer.cpu == "Intel i9"
    assert computer.ram == 32
    assert computer.storage == "1TB SSD"
    assert computer.gpu == "NVIDIA RTX 4090"
    assert computer.os == "Ubuntu Linux"
    assert len(computer.peripherals) == 2
    assert "Mechanical Keyboard" in computer.peripherals


def test_computer_specifications():
    """Test computer specifications string formatting."""
    builder = ComputerBuilder()
    computer = builder.set_cpu("AMD Ryzen 9").set_ram(64).build()

    specs = computer.get_specifications()
    assert "CPU: AMD Ryzen 9" in specs
    assert "RAM: 64GB" in specs


def test_computer_builder_reset():
    """Test builder reset functionality."""
    builder = ComputerBuilder()
    computer1 = builder.set_cpu("Intel i5").build()

    builder.reset()
    computer2 = builder.set_cpu("AMD Ryzen 7").build()

    assert computer1.cpu == "Intel i5"
    assert computer2.cpu == "AMD Ryzen 7"
    assert computer1 is not computer2


def test_computer_empty_specifications():
    """Test specifications for an empty computer."""
    computer = ComputerBuilder().build()
    assert computer.get_specifications() == "No specifications set"


def test_house_builder_basic():
    """Test building a basic house."""
    builder = HouseBuilder()
    house = (builder
             .set_foundation("Concrete")
             .set_walls("Wood")
             .set_windows(3)
             .set_doors(1)
             .build())

    assert house.foundation == "Concrete"
    assert house.walls == "Wood"
    assert house.windows == 3
    assert house.doors == 1
    assert house.garage is False
    assert house.garden is False


def test_house_builder_with_extras():
    """Test building a house with garage and garden."""
    builder = HouseBuilder()
    house = (builder
             .set_foundation("Deep foundation")
             .add_garage()
             .add_garden()
             .build())

    assert house.garage is True
    assert house.garden is True


def test_house_simple_director():
    """Test the simple house director method."""
    builder = HouseBuilder()
    house = builder.build_simple_house()

    assert house.foundation == "Concrete slab"
    assert house.walls == "Brick"
    assert house.roof == "Asphalt shingles"
    assert house.windows == 4
    assert house.doors == 1
    assert house.garage is False


def test_house_luxury_director():
    """Test the luxury house director method."""
    builder = HouseBuilder()
    house = builder.build_luxury_house()

    assert house.foundation == "Deep foundation"
    assert house.walls == "Stone"
    assert house.roof == "Tile"
    assert house.windows == 12
    assert house.doors == 3
    assert house.garage is True
    assert house.garden is True


def test_house_describe():
    """Test house description."""
    builder = HouseBuilder()
    house = builder.set_foundation("Concrete").set_walls("Brick").build()

    description = house.describe()
    assert "Foundation: Concrete" in description
    assert "Walls: Brick" in description


def test_builder_method_chaining():
    """Test that builder methods properly chain."""
    builder = ComputerBuilder()
    result = builder.set_cpu("Intel").set_ram(16).set_storage("512GB")

    assert result is builder
    assert builder._computer.cpu == "Intel"
    assert builder._computer.ram == 16
    assert builder._computer.storage == "512GB"
