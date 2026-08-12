"""
Decorator Pattern Example: HTTP Middleware Stack

Demonstrates using the Decorator pattern to build a middleware system
where multiple layers of functionality can be added to request processing.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class Request:
    """HTTP Request object"""

    def __init__(self, method: str, path: str, headers: dict[str, str] | None = None):
        self.method = method
        self.path = path
        self.headers = headers or {}
        self.user: str | None = None
        self.start_time: datetime | None = None
        self.metadata: dict[str, Any] = {}


class Response:
    """HTTP Response object"""

    def __init__(
        self, status_code: int, body: str, headers: dict[str, str] | None = None
    ):
        self.status_code = status_code
        self.body = body
        self.headers = headers or {}


class RequestHandler(ABC):
    """Abstract request handler interface"""

    @abstractmethod
    def handle(self, request: Request) -> Response:
        """Handle the request and return a response"""


class BaseRequestHandler(RequestHandler):
    """Base request handler that returns simple responses"""

    def handle(self, request: Request) -> Response:
        print(f"\n[HANDLER] Processing {request.method} {request.path}")

        # Simulate different endpoints
        if request.path == "/api/users":
            body = '{"users": ["Alice", "Bob", "Charlie"]}'
            return Response(200, body)
        if request.path == "/api/profile":
            if request.user:
                body = (
                    f'{{"user": "{request.user}", '
                    f'"email": "{request.user}@example.com"}}'
                )
                return Response(200, body)
            return Response(401, '{"error": "Unauthorized"}')
        return Response(404, '{"error": "Not Found"}')


class RequestHandlerDecorator(RequestHandler):
    """Base decorator for request handlers"""

    def __init__(self, handler: RequestHandler):
        self._handler = handler

    def handle(self, request: Request) -> Response:
        return self._handler.handle(request)


class LoggingMiddleware(RequestHandlerDecorator):
    """Logs all requests and responses"""

    def handle(self, request: Request) -> Response:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[LOGGING] {timestamp} - Incoming {request.method} {request.path}")

        response = self._handler.handle(request)

        print(
            f"[LOGGING] {timestamp} - Response {response.status_code} "
            f"({len(response.body)} bytes)"
        )

        return response


class AuthenticationMiddleware(RequestHandlerDecorator):
    """Validates authentication tokens"""

    def handle(self, request: Request) -> Response:
        print("\n[AUTH] Checking authentication...")

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            print("[AUTH] No authorization header found")
            if request.path.startswith("/api/profile"):
                return Response(401, '{"error": "Authentication required"}')
        else:
            # Simulate token validation
            token = auth_header.replace("Bearer ", "")
            request.user = self._validate_token(token)
            print(f"[AUTH] Authenticated as: {request.user}")

        return self._handler.handle(request)

    def _validate_token(self, token: str) -> str:
        """Simulate token validation"""
        # In real app, this would validate JWT or session token
        token_map = {"token123": "alice", "token456": "bob", "token789": "charlie"}
        return token_map.get(token, "guest")


class RateLimitMiddleware(RequestHandlerDecorator):
    """Implements rate limiting"""

    def __init__(self, handler: RequestHandler, max_requests: int = 10):
        super().__init__(handler)
        self.max_requests = max_requests
        self.request_counts: dict[str, int] = {}

    def handle(self, request: Request) -> Response:
        print("\n[RATE LIMIT] Checking rate limit...")

        # Use IP address or user for rate limiting
        identifier = request.headers.get("X-Forwarded-For", "127.0.0.1")
        current_count = self.request_counts.get(identifier, 0)

        if current_count >= self.max_requests:
            print(f"[RATE LIMIT] Limit exceeded for {identifier}")
            return Response(429, '{"error": "Too Many Requests"}')

        self.request_counts[identifier] = current_count + 1
        print(
            f"[RATE LIMIT] Request {current_count + 1}/{self.max_requests} "
            f"for {identifier}"
        )

        return self._handler.handle(request)


class TimingMiddleware(RequestHandlerDecorator):
    """Measures request processing time"""

    def handle(self, request: Request) -> Response:
        start_time = datetime.now()
        print(f"\n[TIMING] Request started at {start_time.strftime('%H:%M:%S.%f')}")

        response = self._handler.handle(request)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds() * 1000
        print(f"[TIMING] Request completed in {duration:.2f}ms")

        response.headers["X-Response-Time"] = f"{duration:.2f}ms"

        return response


class CorsMiddleware(RequestHandlerDecorator):
    """Adds CORS headers to responses"""

    def handle(self, request: Request) -> Response:
        print("\n[CORS] Adding CORS headers...")

        response = self._handler.handle(request)

        # Add CORS headers
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

        print("[CORS] CORS headers added")

        return response


def main():
    """Demonstrate the Decorator pattern with middleware stack"""

    print("=" * 70)
    print("Decorator Pattern: HTTP Middleware Stack")
    print("=" * 70)

    # Scenario 1: Basic handler without middleware
    print("\n\n--- Scenario 1: No Middleware ---")
    basic_handler = BaseRequestHandler()
    request1 = Request("GET", "/api/users")
    response1 = basic_handler.handle(request1)
    print(f"Response: {response1.status_code} - {response1.body}")

    # Scenario 2: Add logging middleware
    print("\n\n" + "=" * 70)
    print("--- Scenario 2: With Logging Middleware ---")
    print("=" * 70)
    logged_handler = LoggingMiddleware(BaseRequestHandler())
    request2 = Request("GET", "/api/users")
    logged_handler.handle(request2)

    # Scenario 3: Stack multiple middleware
    print("\n\n" + "=" * 70)
    print("--- Scenario 3: Multiple Middleware Layers ---")
    print("=" * 70)

    # Build middleware stack: Timing -> Logging -> Auth -> Rate Limit -> Handler
    handler = BaseRequestHandler()
    handler = RateLimitMiddleware(handler, max_requests=5)
    handler = AuthenticationMiddleware(handler)
    handler = LoggingMiddleware(handler)
    handler = TimingMiddleware(handler)
    handler = CorsMiddleware(handler)

    # Make authenticated request
    print("\n>> Request 1: Authenticated user accessing profile")
    request3 = Request(
        "GET",
        "/api/profile",
        headers={"Authorization": "Bearer token123", "X-Forwarded-For": "192.168.1.1"},
    )
    response3 = handler.handle(request3)
    print(f"\nFinal Response: {response3.status_code}")
    print(f"Body: {response3.body}")
    print(f"Headers: {response3.headers}")

    # Make unauthenticated request
    print("\n\n>> Request 2: Unauthenticated user accessing profile")
    request4 = Request(
        "GET", "/api/profile", headers={"X-Forwarded-For": "192.168.1.2"}
    )
    response4 = handler.handle(request4)
    print(f"\nFinal Response: {response4.status_code}")
    print(f"Body: {response4.body}")

    # Test rate limiting
    print("\n\n" + "=" * 70)
    print("--- Scenario 4: Rate Limiting ---")
    print("=" * 70)

    rate_limited_handler = RateLimitMiddleware(BaseRequestHandler(), max_requests=3)

    for i in range(5):
        print(f"\n>> Request {i + 1}")
        request = Request(
            "GET", "/api/users", headers={"X-Forwarded-For": "192.168.1.100"}
        )
        response = rate_limited_handler.handle(request)
        print(f"Status: {response.status_code}")

    # Demonstrate middleware composition
    print("\n\n" + "=" * 70)
    print("Benefits of Decorator Pattern:")
    print("- Add functionality dynamically at runtime")
    print("- Stack multiple behaviors in any order")
    print("- Each middleware is independent and reusable")
    print("- Easy to add/remove middleware without changing handler")
    print("- Follows Open/Closed Principle")
    print("=" * 70)

    print("\n\nMiddleware Stack Visualization:")
    print("Request → CORS → Timing → Logging → Auth → Rate Limit → Handler")
    print("Response ← CORS ← Timing ← Logging ← Auth ← Rate Limit ← Handler")


if __name__ == "__main__":
    main()
