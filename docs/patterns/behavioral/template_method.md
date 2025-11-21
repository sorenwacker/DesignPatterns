# Template Method Pattern

**Category:** Behavioral Pattern

## Intent

Define the skeleton of an algorithm in a base class, allowing subclasses to override specific steps of the algorithm without changing its structure. The Template Method pattern promotes code reuse and enforces a consistent algorithm structure across different implementations.

## Problem

When multiple classes share similar algorithms with slight variations, duplication leads to:

- Code duplication across similar implementations
- Inconsistent algorithm structures
- Difficulty maintaining common steps
- No enforcement of algorithm sequence
- Violation of DRY (Don't Repeat Yourself) principle
- Hard to modify shared logic

## When to Use

Use the Template Method pattern when:

- **Common algorithm structure**: Multiple classes share same algorithm skeleton
- **Varying steps**: Some steps vary between implementations
- **Enforce structure**: Want to enforce specific algorithm sequence
- **Code reuse**: Common steps should be implemented once
- **Hook methods**: Subclasses need optional extension points
- **Framework design**: Building frameworks with customizable behavior

## When NOT to Use

Avoid the Template Method pattern when:

- **Unique algorithms**: Each implementation is completely different
- **Composition preferred**: Composition would be more flexible than inheritance
- **Simple operations**: No shared logic between implementations
- **Deep inheritance**: Would create deep inheritance hierarchies
- **Frequent changes**: Algorithm structure changes frequently

## Structure

The Template Method pattern involves:

- **Abstract Class**: Defines template method and primitive operations
- **Template Method**: Defines algorithm skeleton calling primitive operations
- **Primitive Operations**: Abstract methods implemented by subclasses
- **Hook Methods**: Optional operations with default implementations
- **Concrete Classes**: Implement primitive operations

## Implementation

### Data Mining Example

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
        self.send_report(analysis)
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

    def send_report(self, analysis: dict[str, str]) -> None:
        """Send the analysis report.

        This is a hook method with a default implementation.
        """
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

    def send_report(self, analysis: dict[str, str]) -> None:
        """Send CSV mining report."""
        pass

class XMLDataMiner(DataMiner):
    """Concrete data miner for XML files."""

    def open_file(self, path: str) -> str:
        """Open XML file."""
        return f"XML({path})"

    def extract_data(self, data: str) -> str:
        """Extract data from XML."""
        return f"Parsed XML from {data}"

    def close_file(self, data: str) -> None:
        """Close XML file."""
        pass

    def analyze_data(self, data: str) -> dict[str, str]:
        """Analyze XML data with custom logic."""
        return {"status": "XML analyzed", "data": data, "format": "XML"}
```

### Beverage Preparation Example

```python
class Beverage(ABC):
    """Abstract class for making beverages using template method."""

    def prepare(self) -> list[str]:
        """Template method for preparing a beverage."""
        steps = []
        steps.append(self.boil_water())
        steps.append(self.brew())
        steps.append(self.pour_in_cup())
        if self.wants_condiments():
            steps.append(self.add_condiments())
        return steps

    def boil_water(self) -> str:
        """Boil water."""
        return "Boiling water"

    @abstractmethod
    def brew(self) -> str:
        """Brew the beverage."""
        pass

    def pour_in_cup(self) -> str:
        """Pour in cup."""
        return "Pouring into cup"

    @abstractmethod
    def add_condiments(self) -> str:
        """Add condiments."""
        pass

    def wants_condiments(self) -> bool:
        """Hook method to determine if condiments should be added."""
        return True

class Tea(Beverage):
    """Concrete beverage: Tea."""

    def brew(self) -> str:
        """Brew tea."""
        return "Steeping tea"

    def add_condiments(self) -> str:
        """Add lemon."""
        return "Adding lemon"

class Coffee(Beverage):
    """Concrete beverage: Coffee."""

    def brew(self) -> str:
        """Brew coffee."""
        return "Dripping coffee through filter"

    def add_condiments(self) -> str:
        """Add sugar and milk."""
        return "Adding sugar and milk"

class BlackCoffee(Beverage):
    """Concrete beverage: Black coffee without condiments."""

    def brew(self) -> str:
        """Brew coffee."""
        return "Dripping coffee through filter"

    def add_condiments(self) -> str:
        """No condiments for black coffee."""
        return ""

    def wants_condiments(self) -> bool:
        """Black coffee doesn't want condiments."""
        return False
```

## Usage Example

```python
# PDF data mining
pdf_miner = PDFDataMiner()
result = pdf_miner.mine("document.pdf")
print(result)  # {'status': 'analyzed', 'data': 'Extracted from PDF(document.pdf)'}

# CSV data mining
csv_miner = CSVDataMiner()
result = csv_miner.mine("data.csv")
print(result)  # {'status': 'analyzed', 'data': 'Parsed CSV(data.csv)'}

# XML data mining with custom analysis
xml_miner = XMLDataMiner()
result = xml_miner.mine("config.xml")
print(result)  # {'status': 'XML analyzed', 'data': '...', 'format': 'XML'}

# Beverage preparation
tea = Tea()
steps = tea.prepare()
print(steps)
# ['Boiling water', 'Steeping tea', 'Pouring into cup', 'Adding lemon']

coffee = Coffee()
steps = coffee.prepare()
print(steps)
# ['Boiling water', 'Dripping coffee through filter', 'Pouring into cup', 'Adding sugar and milk']

black_coffee = BlackCoffee()
steps = black_coffee.prepare()
print(steps)
# ['Boiling water', 'Dripping coffee through filter', 'Pouring into cup']
```

## Key Benefits

1. **Code reuse**: Common code is in one place
2. **Consistent structure**: Algorithm structure is consistent across implementations
3. **Protected template**: Template method prevents algorithm modification
4. **Extensibility**: Easy to add new implementations
5. **Hook methods**: Optional extension points for subclasses
6. **Inversion of control**: Framework calls subclass methods (Hollywood Principle)

## Drawbacks

1. **Inheritance coupling**: Tight coupling through inheritance
2. **Liskov violation**: Subclass constraints may violate substitution principle
3. **Limited flexibility**: Algorithm structure is fixed
4. **Maintenance**: Changes to template affect all subclasses
5. **Deep hierarchies**: Can lead to deep inheritance trees

## Real-World Examples

- **Framework hooks**: Django views, React lifecycle methods
- **Data processing pipelines**: ETL (Extract, Transform, Load) operations
- **Testing frameworks**: setUp, test, tearDown methods
- **Build systems**: Pre-build, build, post-build steps
- **Game loops**: Initialize, update, render, cleanup
- **Document generation**: Header, body, footer sections
- **HTTP request handling**: Parse, validate, process, respond

## Related Patterns

- **Strategy**: Strategy uses composition vs inheritance in Template Method
- **Factory Method**: Often called by template methods
- **Hook Method**: Template Method defines hook methods for customization

## API Reference

::: design_patterns.behavioral.template_method
    options:
      show_root_heading: true
      show_source: true
