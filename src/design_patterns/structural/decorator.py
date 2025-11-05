"""Decorator Pattern Module

The Decorator pattern attaches additional responsibilities to an object dynamically.
Decorators provide a flexible alternative to subclassing for extending functionality.
This pattern allows behavior to be added to individual objects without affecting other
objects of the same class.

Example:
    Decorating a coffee order:

    ```python
    coffee = SimpleCoffee()
    coffee = MilkDecorator(coffee)
    coffee = SugarDecorator(coffee)

    print(coffee.get_description())  # "Simple Coffee, Milk, Sugar"
    print(coffee.get_cost())  # 3.0
    ```
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Coffee(ABC):
    """Abstract base class for coffee."""

    @abstractmethod
    def get_cost(self) -> float:
        """Get the cost of the coffee.

        Returns:
            The cost in dollars.
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Get the description of the coffee.

        Returns:
            Coffee description.
        """
        pass


class SimpleCoffee(Coffee):
    """Basic coffee without any additions."""

    def get_cost(self) -> float:
        """Get base coffee cost.

        Returns:
            Base cost of 1.0.
        """
        return 1.0

    def get_description(self) -> str:
        """Get base coffee description.

        Returns:
            Description string.
        """
        return "Simple Coffee"


class CoffeeDecorator(Coffee):
    """Base decorator class for coffee add-ons."""

    def __init__(self, coffee: Coffee) -> None:
        """Initialize decorator with a coffee instance.

        Args:
            coffee: The coffee to decorate.
        """
        self._coffee = coffee

    def get_cost(self) -> float:
        """Get cost including this decorator.

        Returns:
            Total cost.
        """
        return self._coffee.get_cost()

    def get_description(self) -> str:
        """Get description including this decorator.

        Returns:
            Complete description.
        """
        return self._coffee.get_description()


class MilkDecorator(CoffeeDecorator):
    """Decorator that adds milk to coffee."""

    def get_cost(self) -> float:
        """Get cost with milk added.

        Returns:
            Cost plus 0.5 for milk.
        """
        return self._coffee.get_cost() + 0.5

    def get_description(self) -> str:
        """Get description with milk.

        Returns:
            Description with milk added.
        """
        return self._coffee.get_description() + ", Milk"


class SugarDecorator(CoffeeDecorator):
    """Decorator that adds sugar to coffee."""

    def get_cost(self) -> float:
        """Get cost with sugar added.

        Returns:
            Cost plus 0.2 for sugar.
        """
        return self._coffee.get_cost() + 0.2

    def get_description(self) -> str:
        """Get description with sugar.

        Returns:
            Description with sugar added.
        """
        return self._coffee.get_description() + ", Sugar"


class VanillaDecorator(CoffeeDecorator):
    """Decorator that adds vanilla to coffee."""

    def get_cost(self) -> float:
        """Get cost with vanilla added.

        Returns:
            Cost plus 0.7 for vanilla.
        """
        return self._coffee.get_cost() + 0.7

    def get_description(self) -> str:
        """Get description with vanilla.

        Returns:
            Description with vanilla added.
        """
        return self._coffee.get_description() + ", Vanilla"


class WhippedCreamDecorator(CoffeeDecorator):
    """Decorator that adds whipped cream to coffee."""

    def get_cost(self) -> float:
        """Get cost with whipped cream added.

        Returns:
            Cost plus 0.8 for whipped cream.
        """
        return self._coffee.get_cost() + 0.8

    def get_description(self) -> str:
        """Get description with whipped cream.

        Returns:
            Description with whipped cream added.
        """
        return self._coffee.get_description() + ", Whipped Cream"


class DataSource(ABC):
    """Abstract interface for data sources."""

    @abstractmethod
    def write_data(self, data: str) -> None:
        """Write data to the source.

        Args:
            data: The data to write.
        """
        pass

    @abstractmethod
    def read_data(self) -> str:
        """Read data from the source.

        Returns:
            The data.
        """
        pass


class FileDataSource(DataSource):
    """Basic file data source."""

    def __init__(self, filename: str) -> None:
        """Initialize file data source.

        Args:
            filename: The file name.
        """
        self.filename = filename
        self._data: str = ""

    def write_data(self, data: str) -> None:
        """Write data to file.

        Args:
            data: Data to write.
        """
        self._data = data

    def read_data(self) -> str:
        """Read data from file.

        Returns:
            The stored data.
        """
        return self._data


class DataSourceDecorator(DataSource):
    """Base decorator for data sources."""

    def __init__(self, source: DataSource) -> None:
        """Initialize decorator.

        Args:
            source: The data source to decorate.
        """
        self._source = source

    def write_data(self, data: str) -> None:
        """Write data through decorator.

        Args:
            data: Data to write.
        """
        self._source.write_data(data)

    def read_data(self) -> str:
        """Read data through decorator.

        Returns:
            The data.
        """
        return self._source.read_data()


class EncryptionDecorator(DataSourceDecorator):
    """Decorator that adds encryption to data operations."""

    def write_data(self, data: str) -> None:
        """Write encrypted data.

        Args:
            data: Data to encrypt and write.
        """
        encrypted = self._encrypt(data)
        self._source.write_data(encrypted)

    def read_data(self) -> str:
        """Read and decrypt data.

        Returns:
            Decrypted data.
        """
        encrypted = self._source.read_data()
        return self._decrypt(encrypted)

    def _encrypt(self, data: str) -> str:
        """Simple encryption (reversed string).

        Args:
            data: Data to encrypt.

        Returns:
            Encrypted data.
        """
        return data[::-1]

    def _decrypt(self, data: str) -> str:
        """Simple decryption (reverse the reversed string).

        Args:
            data: Data to decrypt.

        Returns:
            Decrypted data.
        """
        return data[::-1]


class CompressionDecorator(DataSourceDecorator):
    """Decorator that adds compression to data operations."""

    def write_data(self, data: str) -> None:
        """Write compressed data.

        Args:
            data: Data to compress and write.
        """
        compressed = self._compress(data)
        self._source.write_data(compressed)

    def read_data(self) -> str:
        """Read and decompress data.

        Returns:
            Decompressed data.
        """
        compressed = self._source.read_data()
        return self._decompress(compressed)

    def _compress(self, data: str) -> str:
        """Simple compression simulation (prefix with marker).

        Args:
            data: Data to compress.

        Returns:
            Compressed data.
        """
        return f"[COMPRESSED]{data}"

    def _decompress(self, data: str) -> str:
        """Simple decompression simulation (remove prefix).

        Args:
            data: Data to decompress.

        Returns:
            Decompressed data.
        """
        if data.startswith("[COMPRESSED]"):
            return data[12:]
        return data
