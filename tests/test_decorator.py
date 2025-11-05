"""Tests for the Decorator pattern."""

from design_patterns.structural.decorator import (
    CompressionDecorator,
    EncryptionDecorator,
    FileDataSource,
    MilkDecorator,
    SimpleCoffee,
    SugarDecorator,
    VanillaDecorator,
    WhippedCreamDecorator,
)


def test_simple_coffee():
    """Test basic coffee without decorators."""
    coffee = SimpleCoffee()
    assert coffee.get_cost() == 1.0
    assert coffee.get_description() == "Simple Coffee"


def test_coffee_with_milk():
    """Test coffee with milk decorator."""
    coffee = SimpleCoffee()
    coffee = MilkDecorator(coffee)

    assert coffee.get_cost() == 1.5
    assert coffee.get_description() == "Simple Coffee, Milk"


def test_coffee_with_sugar():
    """Test coffee with sugar decorator."""
    coffee = SimpleCoffee()
    coffee = SugarDecorator(coffee)

    assert coffee.get_cost() == 1.2
    assert coffee.get_description() == "Simple Coffee, Sugar"


def test_coffee_with_multiple_decorators():
    """Test coffee with multiple decorators."""
    coffee = SimpleCoffee()
    coffee = MilkDecorator(coffee)
    coffee = SugarDecorator(coffee)
    coffee = VanillaDecorator(coffee)

    assert coffee.get_cost() == 2.4
    assert coffee.get_description() == "Simple Coffee, Milk, Sugar, Vanilla"


def test_coffee_with_whipped_cream():
    """Test coffee with whipped cream."""
    coffee = SimpleCoffee()
    coffee = WhippedCreamDecorator(coffee)

    assert coffee.get_cost() == 1.8
    assert coffee.get_description() == "Simple Coffee, Whipped Cream"


def test_coffee_all_decorators():
    """Test coffee with all decorators."""
    coffee = SimpleCoffee()
    coffee = MilkDecorator(coffee)
    coffee = SugarDecorator(coffee)
    coffee = VanillaDecorator(coffee)
    coffee = WhippedCreamDecorator(coffee)

    assert coffee.get_cost() == 3.2
    assert "Milk" in coffee.get_description()
    assert "Sugar" in coffee.get_description()
    assert "Vanilla" in coffee.get_description()
    assert "Whipped Cream" in coffee.get_description()


def test_coffee_double_milk():
    """Test coffee with milk added twice."""
    coffee = SimpleCoffee()
    coffee = MilkDecorator(coffee)
    coffee = MilkDecorator(coffee)

    assert coffee.get_cost() == 2.0
    assert coffee.get_description() == "Simple Coffee, Milk, Milk"


def test_file_data_source():
    """Test basic file data source."""
    file = FileDataSource("test.txt")
    file.write_data("Hello World")

    assert file.read_data() == "Hello World"


def test_file_with_encryption():
    """Test file data source with encryption."""
    file = FileDataSource("test.txt")
    file = EncryptionDecorator(file)

    file.write_data("Secret Message")
    assert file.read_data() == "Secret Message"


def test_file_with_compression():
    """Test file data source with compression."""
    file = FileDataSource("test.txt")
    file = CompressionDecorator(file)

    file.write_data("Large Data")
    assert file.read_data() == "Large Data"


def test_file_with_encryption_and_compression():
    """Test file with both encryption and compression."""
    file = FileDataSource("test.txt")
    file = EncryptionDecorator(file)
    file = CompressionDecorator(file)

    original_data = "Secret Large Data"
    file.write_data(original_data)
    assert file.read_data() == original_data


def test_file_different_decorator_order():
    """Test file with decorators in different order."""
    file1 = FileDataSource("test1.txt")
    file1 = CompressionDecorator(file1)
    file1 = EncryptionDecorator(file1)

    file2 = FileDataSource("test2.txt")
    file2 = EncryptionDecorator(file2)
    file2 = CompressionDecorator(file2)

    data = "Test Data"
    file1.write_data(data)
    file2.write_data(data)

    assert file1.read_data() == data
    assert file2.read_data() == data


def test_encryption_decorator_internals():
    """Test encryption decorator encryption/decryption."""
    file = FileDataSource("test.txt")
    enc = EncryptionDecorator(file)

    encrypted = enc._encrypt("hello")
    assert encrypted == "olleh"

    decrypted = enc._decrypt(encrypted)
    assert decrypted == "hello"


def test_compression_decorator_internals():
    """Test compression decorator compression/decompression."""
    file = FileDataSource("test.txt")
    comp = CompressionDecorator(file)

    compressed = comp._compress("data")
    assert compressed == "[COMPRESSED]data"

    decompressed = comp._decompress(compressed)
    assert decompressed == "data"
