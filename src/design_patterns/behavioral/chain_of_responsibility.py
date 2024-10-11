"""
Chain of Responsibility Pattern Example

This module demonstrates the Chain of Responsibility design pattern in Python.
It defines a series of handler classes that process requests. Each handler can
either handle a request or pass it to the next handler in the chain.

Example:
    Creating a chain of handlers and testing it:
    
    ```
    # Creating the chain of responsibility
    handler_chain = ApprovalRequestHandler(EscalationRequestHandler())

    # Testing the chain with different requests
    print(handler_chain.handle("ApprovalRequest"))  # Output: ApprovalRequestHandler handled ApprovalRequest
    print(handler_chain.handle("EscalationRequest"))  # Output: EscalationRequestHandler handled EscalationRequest
    print(handler_chain.handle("FeedbackRequest"))  # Output: No handler for FeedbackRequest
    ```

Classes:
    RequestHandler: Base class for handling requests.
    ApprovalRequestHandler: Handles approval requests.
    EscalationRequestHandler: Handles escalation requests.
"""

from typing import Optional


class RequestHandler:
    """Base class for handling requests in a chain of responsibility.

    This class defines the interface for handling requests and allows
    for the creation of a chain of handlers. Each handler can process
    specific requests or pass them to the next handler in the chain.
    """

    def __init__(self, successor: Optional['RequestHandler'] = None) -> None:
        """Initializes the handler with an optional successor.

        Args:
            successor (Optional[RequestHandler]): The next handler in the chain.
        """
        self.successor = successor

    def handle(self, request: str) -> str:
        """Handles the request or passes it to the next handler.

        Args:
            request (str): The request to be handled.

        Returns:
            str: The result of the request.
        """
        if self.successor:
            return self.successor.handle(request)
        return f"No handler for {request}"


class ApprovalRequestHandler(RequestHandler):
    """Handler that processes approval requests.

    This handler is responsible for handling requests related to approvals.
    """

    def handle(self, request: str) -> str:
        """Handles specific requests for ApprovalRequestHandler.

        Args:
            request (str): The request to be handled.

        Returns:
            str: The result of handling the request.
        """
        if request == "ApprovalRequest":
            return "ApprovalRequestHandler handled ApprovalRequest"
        return super().handle(request)


class EscalationRequestHandler(RequestHandler):
    """Handler that processes escalation requests.

    This handler is responsible for handling requests related to escalations.
    """

    def handle(self, request: str) -> str:
        """Handles specific requests for EscalationRequestHandler.

        Args:
            request (str): The request to be handled.

        Returns:
            str: The result of handling the request.
        """
        if request == "EscalationRequest":
            return "EscalationRequestHandler handled EscalationRequest"
        return super().handle(request)

# The example usage for testing the chain of handlers is found in the module docstring.
