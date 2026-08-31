"""Tests for the Adapter pattern."""

import pytest

from design_patterns.structural.adapter import (
    LegacyLogger,
    LoggerAdapter,
    LoggerInterface,
)


def test_legacy_logger_writes_log(capsys):
    """Test that LegacyLogger writes logs correctly."""
    logger = LegacyLogger()
    logger.write_log("Test message")
    captured = capsys.readouterr()
    assert captured.out == "Legacy Log: Test message\n"


def test_logger_adapter_implements_interface():
    """Test that LoggerAdapter implements LoggerInterface."""
    legacy_logger = LegacyLogger()
    adapter = LoggerAdapter(legacy_logger)
    assert isinstance(adapter, LoggerInterface)


def test_logger_adapter_log_info(capsys):
    """Test that LoggerAdapter logs info messages."""
    legacy_logger = LegacyLogger()
    adapter = LoggerAdapter(legacy_logger)
    adapter.log_info("Information message")
    captured = capsys.readouterr()
    assert captured.out == "Legacy Log: INFO: Information message\n"


def test_logger_adapter_log_error(capsys):
    """Test that LoggerAdapter logs error messages."""
    legacy_logger = LegacyLogger()
    adapter = LoggerAdapter(legacy_logger)
    adapter.log_error("Error message")
    captured = capsys.readouterr()
    assert captured.out == "Legacy Log: ERROR: Error message\n"


def test_logger_adapter_multiple_messages(capsys):
    """Test that LoggerAdapter handles multiple log messages."""
    legacy_logger = LegacyLogger()
    adapter = LoggerAdapter(legacy_logger)
    adapter.log_info("First message")
    adapter.log_error("Second message")
    adapter.log_info("Third message")
    captured = capsys.readouterr()
    expected = (
        "Legacy Log: INFO: First message\n"
        "Legacy Log: ERROR: Second message\n"
        "Legacy Log: INFO: Third message\n"
    )
    assert captured.out == expected


def test_logger_interface_cannot_be_instantiated():
    """The target interface is abstract; the adapter is the concrete logger."""
    with pytest.raises(TypeError, match="abstract"):
        LoggerInterface()  # type: ignore[abstract]
