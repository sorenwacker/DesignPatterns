"""Tests for the Template Method pattern."""

from design_patterns.behavioral.template_method import (
    BlackCoffee,
    Coffee,
    CSVDataMiner,
    PDFDataMiner,
    Tea,
    XMLDataMiner,
)


def test_pdf_data_miner():
    """Test PDF data mining."""
    miner = PDFDataMiner()
    result = miner.mine("document.pdf")

    assert result["status"] == "analyzed"
    assert "PDF(document.pdf)" in result["data"]


def test_csv_data_miner():
    """Test CSV data mining."""
    miner = CSVDataMiner()
    result = miner.mine("data.csv")

    assert result["status"] == "analyzed"
    assert "CSV(data.csv)" in result["data"]


def test_xml_data_miner():
    """Test XML data mining with custom analysis."""
    miner = XMLDataMiner()
    result = miner.mine("config.xml")

    assert result["status"] == "XML analyzed"
    assert result["format"] == "XML"
    assert "XML(config.xml)" in result["data"]


def test_pdf_extraction():
    """Test PDF-specific extraction."""
    miner = PDFDataMiner()
    data = miner.open_file("test.pdf")
    extracted = miner.extract_data(data)

    assert "Extracted from PDF(test.pdf)" in extracted


def test_csv_extraction():
    """Test CSV-specific extraction."""
    miner = CSVDataMiner()
    data = miner.open_file("test.csv")
    extracted = miner.extract_data(data)

    assert "Parsed CSV(test.csv)" in extracted


def test_tea_preparation():
    """Test tea preparation steps."""
    tea = Tea()
    steps = tea.prepare()

    assert len(steps) == 4
    assert "Boiling water" in steps
    assert "Steeping tea" in steps
    assert "Pouring into cup" in steps
    assert "Adding lemon" in steps


def test_coffee_preparation():
    """Test coffee preparation steps."""
    coffee = Coffee()
    steps = coffee.prepare()

    assert len(steps) == 4
    assert "Boiling water" in steps
    assert any("Dripping coffee" in step for step in steps)
    assert "Pouring into cup" in steps
    assert "Adding sugar and milk" in steps


def test_black_coffee_preparation():
    """Test black coffee preparation without condiments."""
    coffee = BlackCoffee()
    steps = coffee.prepare()

    assert len(steps) == 3
    assert "Boiling water" in steps
    assert any("Dripping coffee" in step for step in steps)
    assert "Pouring into cup" in steps
    assert not any("Adding" in step for step in steps)


def test_beverage_hook_method():
    """Test that hook method controls condiment addition."""
    tea = Tea()
    coffee = BlackCoffee()

    assert tea.wants_condiments() is True
    assert coffee.wants_condiments() is False


def test_template_method_structure():
    """Test that template method calls steps in correct order."""
    tea = Tea()
    steps = tea.prepare()

    assert steps[0] == "Boiling water"
    assert steps[1] == "Steeping tea"
    assert steps[2] == "Pouring into cup"
    assert steps[3] == "Adding lemon"


def test_data_miner_default_analysis():
    """Test default analysis implementation."""
    miner = PDFDataMiner()
    analysis = miner.analyze_data("test data")

    assert analysis["status"] == "analyzed"
    assert analysis["data"] == "test data"


def test_xml_custom_analysis():
    """Test that XML miner overrides analysis."""
    miner = XMLDataMiner()
    analysis = miner.analyze_data("test data")

    assert analysis["status"] == "XML analyzed"
    assert analysis["format"] == "XML"
