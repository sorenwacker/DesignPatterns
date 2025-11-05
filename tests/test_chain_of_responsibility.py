"""Tests for the Chain of Responsibility pattern."""

from design_patterns.behavioral.chain_of_responsibility import (
    ApprovalRequestHandler,
    EscalationRequestHandler,
    RequestHandler,
)


def test_approval_handler_handles_approval_request():
    """Test that ApprovalRequestHandler handles approval requests."""
    handler = ApprovalRequestHandler()
    result = handler.handle("ApprovalRequest")
    assert result == "ApprovalRequestHandler handled ApprovalRequest"


def test_escalation_handler_handles_escalation_request():
    """Test that EscalationRequestHandler handles escalation requests."""
    handler = EscalationRequestHandler()
    result = handler.handle("EscalationRequest")
    assert result == "EscalationRequestHandler handled EscalationRequest"


def test_chain_passes_to_successor():
    """Test that requests are passed along the chain."""
    escalation_handler = EscalationRequestHandler()
    approval_handler = ApprovalRequestHandler(escalation_handler)

    result = approval_handler.handle("EscalationRequest")
    assert result == "EscalationRequestHandler handled EscalationRequest"


def test_chain_returns_no_handler_message():
    """Test that unhandled requests return appropriate message."""
    handler = ApprovalRequestHandler()
    result = handler.handle("UnknownRequest")
    assert result == "No handler for UnknownRequest"


def test_full_chain_with_multiple_handlers():
    """Test a complete chain with multiple handlers."""
    handler_chain = ApprovalRequestHandler(EscalationRequestHandler())

    assert handler_chain.handle("ApprovalRequest") == "ApprovalRequestHandler handled ApprovalRequest"
    assert handler_chain.handle("EscalationRequest") == "EscalationRequestHandler handled EscalationRequest"
    assert handler_chain.handle("FeedbackRequest") == "No handler for FeedbackRequest"


def test_base_handler_without_successor():
    """Test base handler without a successor."""
    handler = RequestHandler()
    result = handler.handle("AnyRequest")
    assert result == "No handler for AnyRequest"
