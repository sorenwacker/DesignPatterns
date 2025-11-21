# Chain of Responsibility Pattern

**Category:** Behavioral Pattern

## Intent

Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request. Chain the receiving objects and pass the request along the chain until an object handles it. This pattern allows multiple objects to handle a request without the sender knowing which object will ultimately process it.

## Problem

When multiple objects can handle a request, direct coupling to specific handlers leads to:

- Sender must know which handler to use
- Tight coupling between sender and receivers
- Difficulty adding or removing handlers
- Hard-coded handler selection logic
- Inflexible request processing
- Violation of single responsibility principle

## When to Use

Use the Chain of Responsibility pattern when:

- **Multiple handlers**: More than one object can handle a request
- **Dynamic handlers**: Set of handlers should be determined at runtime
- **Avoid coupling**: Sender shouldn't know which handler processes request
- **Pass along chain**: Request should be passed along until handled
- **Handlers vary**: Different handlers process requests differently
- **Middleware**: Implementing middleware or filter chains
- **Event bubbling**: Events should propagate through hierarchy

## When NOT to Use

Avoid the Chain of Responsibility pattern when:

- **Single handler**: Only one object can handle requests
- **Guaranteed handling**: Every request must be handled (chain might not)
- **Performance critical**: Chain traversal overhead is unacceptable
- **Simple routing**: Direct handler selection is straightforward
- **No fallback needed**: No need for fallback handlers

## Structure

The Chain of Responsibility pattern involves:

- **Handler**: Interface declaring method for handling requests and setting successor
- **Concrete Handlers**: Handle requests or pass to successor
- **Client**: Initiates request to chain
- **Chain**: Linked handlers where each can process or pass request

## Implementation

### Request Handler Example

```python
from typing import Optional

class RequestHandler:
    """Base class for handling requests in a chain of responsibility."""

    def __init__(self, successor: Optional['RequestHandler'] = None) -> None:
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

## Usage Example

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

## Key Benefits

1. **Reduced coupling**: Sender doesn't need to know the receiver
2. **Flexibility**: Easy to add or remove handlers at runtime
3. **Responsibility distribution**: Multiple objects share handling responsibility
4. **Single Responsibility**: Each handler focuses on one type of request
5. **Dynamic configuration**: Chain can be configured at runtime
6. **Fallback mechanism**: Unhandled requests can be caught at chain end

## Drawbacks

1. **No guarantee**: Request might not be handled by any handler
2. **Performance**: Chain traversal can be slow
3. **Debugging**: Hard to track which handler processes request
4. **Chain complexity**: Long chains become difficult to manage
5. **Order dependency**: Handler order may affect results

## Real-World Examples

- **Event handling**: GUI event propagation through widget hierarchy
- **Logging frameworks**: Log messages passing through different handlers
- **HTTP middleware**: Request processing through middleware chain
- **Exception handling**: Try-catch blocks at different levels
- **Support ticket systems**: Tickets escalating through support levels
- **Approval workflows**: Requests passing through approval hierarchy
- **Filter chains**: Servlet filters processing HTTP requests

## Related Patterns

- **Composite**: Often combined with Chain of Responsibility for tree structures
- **Command**: Command objects can be handled by chain
- **Decorator**: Similar structure but different intent

## API Reference

::: design_patterns.behavioral.chain_of_responsibility
    options:
      show_root_heading: true
      show_source: true
