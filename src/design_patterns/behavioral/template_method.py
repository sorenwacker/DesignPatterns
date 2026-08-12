"""Template Method Pattern Module

The Template Method pattern defines the skeleton of an algorithm in a base class,
allowing subclasses to override specific steps of the algorithm without changing
its structure. This pattern promotes code reuse and enforces a consistent algorithm
structure across different implementations.

Example:
    Data mining algorithms with different data formats:

    ```python
    pdf_miner = PDFDataMiner()
    pdf_miner.mine("document.pdf")  # Uses PDF-specific parsing

    csv_miner = CSVDataMiner()
    csv_miner.mine("data.csv")  # Uses CSV-specific parsing
    ```
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class DataMiner(ABC):
    """Abstract class defining the template method for data mining."""

    def mine(self, path: str) -> dict[str, str]:
        """Template method defining the data mining algorithm.

        This method defines the skeleton of the algorithm. Subclasses
        should not override this method.

        Args:
            path: Path to the data file.

        Returns:
            Dictionary containing mining results.
        """
        data = self.open_file(path)
        raw_data = self.extract_data(data)
        analysis = self.analyze_data(raw_data)
        self.close_file(data)
        self.send_report(analysis)
        return analysis

    @abstractmethod
    def open_file(self, path: str) -> str:
        """Open the file.

        Args:
            path: Path to the file.

        Returns:
            File data representation.
        """

    @abstractmethod
    def extract_data(self, data: str) -> str:
        """Extract data from the file.

        Args:
            data: File data.

        Returns:
            Extracted data.
        """

    def analyze_data(self, data: str) -> dict[str, str]:
        """Analyze the extracted data.

        This is a hook method with a default implementation.

        Args:
            data: Extracted data.

        Returns:
            Analysis results.
        """
        return {"status": "analyzed", "data": data}

    @abstractmethod
    def close_file(self, data: str) -> None:
        """Close the file.

        Args:
            data: File data representation.
        """

    # A hook: subclasses may override it, and the default is deliberately empty.
    def send_report(self, analysis: dict[str, str]) -> None:  # noqa: B027
        """Send the analysis report.

        This is a hook method with a default implementation.

        Args:
            analysis: Analysis results.
        """


class PDFDataMiner(DataMiner):
    """Concrete data miner for PDF files."""

    def open_file(self, path: str) -> str:
        """Open PDF file.

        Args:
            path: Path to PDF file.

        Returns:
            PDF file representation.
        """
        return f"PDF({path})"

    def extract_data(self, data: str) -> str:
        """Extract data from PDF.

        Args:
            data: PDF file data.

        Returns:
            Extracted PDF data.
        """
        return f"Extracted from {data}"

    def close_file(self, data: str) -> None:
        """Close PDF file.

        Args:
            data: PDF file data.
        """


class CSVDataMiner(DataMiner):
    """Concrete data miner for CSV files."""

    def open_file(self, path: str) -> str:
        """Open CSV file.

        Args:
            path: Path to CSV file.

        Returns:
            CSV file representation.
        """
        return f"CSV({path})"

    def extract_data(self, data: str) -> str:
        """Extract data from CSV.

        Args:
            data: CSV file data.

        Returns:
            Extracted CSV data.
        """
        return f"Parsed {data}"

    def close_file(self, data: str) -> None:
        """Close CSV file.

        Args:
            data: CSV file data.
        """

    def send_report(self, analysis: dict[str, str]) -> None:
        """Send CSV mining report.

        Args:
            analysis: Analysis results.
        """


class XMLDataMiner(DataMiner):
    """Concrete data miner for XML files."""

    def open_file(self, path: str) -> str:
        """Open XML file.

        Args:
            path: Path to XML file.

        Returns:
            XML file representation.
        """
        return f"XML({path})"

    def extract_data(self, data: str) -> str:
        """Extract data from XML.

        Args:
            data: XML file data.

        Returns:
            Extracted XML data.
        """
        return f"Parsed XML from {data}"

    def close_file(self, data: str) -> None:
        """Close XML file.

        Args:
            data: XML file data.
        """

    def analyze_data(self, data: str) -> dict[str, str]:
        """Analyze XML data with custom logic.

        Args:
            data: Extracted XML data.

        Returns:
            Custom XML analysis.
        """
        return {"status": "XML analyzed", "data": data, "format": "XML"}


class Beverage(ABC):
    """Abstract class for making beverages using template method."""

    def prepare(self) -> list[str]:
        """Template method for preparing a beverage.

        Returns:
            List of preparation steps.
        """
        steps = []
        steps.append(self.boil_water())
        steps.append(self.brew())
        steps.append(self.pour_in_cup())
        if self.wants_condiments():
            steps.append(self.add_condiments())
        return steps

    def boil_water(self) -> str:
        """Boil water.

        Returns:
            Step description.
        """
        return "Boiling water"

    @abstractmethod
    def brew(self) -> str:
        """Brew the beverage.

        Returns:
            Step description.
        """

    def pour_in_cup(self) -> str:
        """Pour in cup.

        Returns:
            Step description.
        """
        return "Pouring into cup"

    @abstractmethod
    def add_condiments(self) -> str:
        """Add condiments.

        Returns:
            Step description.
        """

    def wants_condiments(self) -> bool:
        """Hook method to determine if condiments should be added.

        Returns:
            True if condiments should be added.
        """
        return True


class Tea(Beverage):
    """Concrete beverage: Tea."""

    def brew(self) -> str:
        """Brew tea.

        Returns:
            Brewing step.
        """
        return "Steeping tea"

    def add_condiments(self) -> str:
        """Add lemon.

        Returns:
            Condiment step.
        """
        return "Adding lemon"


class Coffee(Beverage):
    """Concrete beverage: Coffee."""

    def brew(self) -> str:
        """Brew coffee.

        Returns:
            Brewing step.
        """
        return "Dripping coffee through filter"

    def add_condiments(self) -> str:
        """Add sugar and milk.

        Returns:
            Condiment step.
        """
        return "Adding sugar and milk"


class BlackCoffee(Beverage):
    """Concrete beverage: Black coffee without condiments."""

    def brew(self) -> str:
        """Brew coffee.

        Returns:
            Brewing step.
        """
        return "Dripping coffee through filter"

    def add_condiments(self) -> str:
        """No condiments for black coffee.

        Returns:
            Empty string.
        """
        return ""

    def wants_condiments(self) -> bool:
        """Black coffee doesn't want condiments.

        Returns:
            False.
        """
        return False
