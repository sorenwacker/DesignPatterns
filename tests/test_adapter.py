"""Tests for the Adapter pattern."""

import pytest

from design_patterns.structural.adapter import (
    LegacyLogger,
    LoggerAdapter,
    LoggerInterface,
)


def test_legacy_logger_writes_log():
    """The legacy logger formats a line in its own style."""
    assert LegacyLogger().write_log("Test message") == "Legacy Log: Test message"


def test_logger_adapter_implements_interface():
    """The adapter is usable wherever the target interface is expected."""
    assert isinstance(LoggerAdapter(LegacyLogger()), LoggerInterface)


def test_logger_adapter_log_info():
    """An info call becomes a legacy line with the INFO prefix."""
    adapter = LoggerAdapter(LegacyLogger())
    assert adapter.log_info("Information message") == (
        "Legacy Log: INFO: Information message"
    )


def test_logger_adapter_log_error():
    """An error call becomes a legacy line with the ERROR prefix."""
    adapter = LoggerAdapter(LegacyLogger())
    assert adapter.log_error("Error message") == "Legacy Log: ERROR: Error message"


def test_logger_adapter_keeps_no_state_between_messages():
    """Each call is translated on its own."""
    adapter = LoggerAdapter(LegacyLogger())
    lines = [
        adapter.log_info("First message"),
        adapter.log_error("Second message"),
        adapter.log_info("Third message"),
    ]
    assert lines == [
        "Legacy Log: INFO: First message",
        "Legacy Log: ERROR: Second message",
        "Legacy Log: INFO: Third message",
    ]


def test_logger_interface_cannot_be_instantiated():
    """The target interface is abstract; the adapter is the concrete logger."""
    with pytest.raises(TypeError, match="abstract"):
        LoggerInterface()  # type: ignore[abstract]
