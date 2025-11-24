# Template Method Pattern

**Category:** Behavioral Pattern

## Overview

Define the skeleton of an algorithm in a base class, allowing subclasses to override specific steps without changing the algorithm's structure. This pattern promotes code reuse and enforces a consistent algorithm structure across different implementations.

## Usage Guidelines

**Use when:**

- Multiple classes share the same algorithm skeleton
- Some steps vary between implementations
- Want to enforce specific algorithm sequence
- Common steps should be implemented once

**Avoid when:**

- Each implementation is completely different
- Composition would be more flexible than inheritance
- No shared logic between implementations
- Algorithm structure changes frequently

## Implementation

```python
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
        return analysis

    @abstractmethod
    def open_file(self, path: str) -> str:
        """Open the file."""
        pass

    @abstractmethod
    def extract_data(self, data: str) -> str:
        """Extract data from the file."""
        pass

    def analyze_data(self, data: str) -> dict[str, str]:
        """Analyze the extracted data.

        This is a hook method with a default implementation.
        """
        return {"status": "analyzed", "data": data}

    @abstractmethod
    def close_file(self, data: str) -> None:
        """Close the file."""
        pass

class PDFDataMiner(DataMiner):
    """Concrete data miner for PDF files."""

    def open_file(self, path: str) -> str:
        """Open PDF file."""
        return f"PDF({path})"

    def extract_data(self, data: str) -> str:
        """Extract data from PDF."""
        return f"Extracted from {data}"

    def close_file(self, data: str) -> None:
        """Close PDF file."""
        pass

class CSVDataMiner(DataMiner):
    """Concrete data miner for CSV files."""

    def open_file(self, path: str) -> str:
        """Open CSV file."""
        return f"CSV({path})"

    def extract_data(self, data: str) -> str:
        """Extract data from CSV."""
        return f"Parsed {data}"

    def close_file(self, data: str) -> None:
        """Close CSV file."""
        pass
```

### Usage

```python
# PDF data mining
pdf_miner = PDFDataMiner()
result = pdf_miner.mine("document.pdf")
print(result)  # {'status': 'analyzed', 'data': 'Extracted from PDF(document.pdf)'}

# CSV data mining
csv_miner = CSVDataMiner()
result = csv_miner.mine("data.csv")
print(result)  # {'status': 'analyzed', 'data': 'Parsed CSV(data.csv)'}
```

## Trade-offs

**Benefits:**

1. Common code is in one place promoting code reuse
2. Algorithm structure is consistent across implementations
3. Template method prevents algorithm modification
4. Hook methods provide optional extension points

**Drawbacks:**

1. Tight coupling through inheritance
2. Subclass constraints may violate Liskov Substitution Principle
3. Algorithm structure is fixed with limited flexibility
4. Changes to template affect all subclasses

## Real-World Examples

- Framework hooks like Django views, React lifecycle methods
- Data processing pipelines with ETL operations
- Testing frameworks with setUp, test, tearDown methods
- Build systems with pre-build, build, post-build steps

## Related Patterns

- Strategy
- Factory Method
- Hook Method

## API Reference

::: design_patterns.behavioral.template_method
    options:
      show_root_heading: true
      show_source: true
