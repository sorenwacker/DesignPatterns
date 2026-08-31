# Chain of Responsibility Pattern

**Category:** Behavioral Pattern

## Overview

Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request. Chain the receiving objects and pass the request along the chain until an object handles it, allowing multiple objects to handle a request without the sender knowing which object will ultimately process it.

## Usage Guidelines

**Use when:**

- More than one object can handle a request
- Set of handlers should be determined at runtime
- Sender shouldn't know which handler processes the request
- Implementing middleware or filter chains

**Avoid when:**

- Only one object can handle requests
- Every request must be handled with guarantee
- Chain traversal overhead is unacceptable for performance
- Simple routing with direct handler selection is straightforward

## Implementation

```python
from __future__ import annotations

class RequestHandler:
    """Base class for handling requests in a chain of responsibility."""

    def __init__(self, successor: RequestHandler | None = None) -> None:
        """Initializes the handler with an optional successor.

        Args:
            successor: The next handler in the chain.
        """
        self.successor = successor

    def handle(self, request: str) -> str:
        """Handles the request or passes it to the next handler.

        Args:
            request: The request to be handled.

        Returns:
            str: The result of the request.
        """
        if self.successor:
            return self.successor.handle(request)
        return f"No handler for {request}"

class ApprovalRequestHandler(RequestHandler):
    """Handler that processes approval requests."""

    def handle(self, request: str) -> str:
        """Handles specific requests for ApprovalRequestHandler.

        Args:
            request: The request to be handled.

        Returns:
            str: The result of handling the request.
        """
        if request == "ApprovalRequest":
            return "ApprovalRequestHandler handled ApprovalRequest"
        return super().handle(request)

class EscalationRequestHandler(RequestHandler):
    """Handler that processes escalation requests."""

    def handle(self, request: str) -> str:
        """Handles specific requests for EscalationRequestHandler.

        Args:
            request: The request to be handled.

        Returns:
            str: The result of handling the request.
        """
        if request == "EscalationRequest":
            return "EscalationRequestHandler handled EscalationRequest"
        return super().handle(request)
```

### Usage

```python
# Creating the chain of responsibility
escalation_handler = EscalationRequestHandler()
approval_handler = ApprovalRequestHandler(escalation_handler)

# Testing the chain with different requests
print(approval_handler.handle("ApprovalRequest"))
# Output: ApprovalRequestHandler handled ApprovalRequest

print(approval_handler.handle("EscalationRequest"))
# Output: EscalationRequestHandler handled EscalationRequest

print(approval_handler.handle("FeedbackRequest"))
# Output: No handler for FeedbackRequest
```

## Trade-offs

**Benefits:**

1. Reduced coupling as sender doesn't need to know the receiver
2. Flexibility to add or remove handlers at runtime
3. Multiple objects share handling responsibility
4. Single Responsibility Principle with each handler focused on one type

**Drawbacks:**

1. Request might not be handled by any handler
2. Chain traversal can be slow for performance
3. Hard to track which handler processes request for debugging
4. Long chains become difficult to manage

## Real-World Examples

- GUI event propagation through widget hierarchy
- Logging frameworks with messages passing through handlers
- HTTP middleware request processing
- Support ticket escalation systems

## Related Patterns

- Composite
- Command
- Decorator

## API Reference

::: design_patterns.behavioral.chain_of_responsibility
    options:
      show_root_heading: true
      show_source: true
