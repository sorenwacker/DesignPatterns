# Proxy Pattern

**Category:** Structural Pattern

## Overview

Provide a surrogate or placeholder for another object to control access to it. This pattern is used to create a representative object that controls access to another object, which may be remote, expensive to create, or require protection.

## Usage Guidelines

**Use when:**

- Defer expensive object creation until needed (lazy initialization)
- Control access based on permissions or authentication
- Access objects in different address spaces (remote objects)
- Log access to objects or cache results of expensive operations

**Avoid when:**

- Direct access is sufficient and simple
- No access control or lazy loading required
- Proxy overhead is unacceptable for performance
- Can modify original class directly

## Implementation

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

class Image(ABC):
    """Abstract interface for images."""

    @abstractmethod
    def display(self) -> str:
        """Display the image."""
        pass

    @abstractmethod
    def get_filename(self) -> str:
        """Get the image filename."""
        pass

class RealImage(Image):
    """Real image that is expensive to load."""

    def __init__(self, filename: str) -> None:
        """Initialize and load the image."""
        self.filename = filename
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        """Simulate expensive loading operation."""
        pass

    def display(self) -> str:
        """Display the image."""
        return f"Displaying {self.filename}"

    def get_filename(self) -> str:
        """Get filename."""
        return self.filename

class ImageProxy(Image):
    """Virtual proxy for lazy loading images."""

    def __init__(self, filename: str) -> None:
        """Initialize proxy without loading image."""
        self.filename = filename
        self._real_image: Optional[RealImage] = None

    def display(self) -> str:
        """Display image, loading it if necessary."""
        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        return self._real_image.display()

    def get_filename(self) -> str:
        """Get filename without loading image."""
        return self.filename

    def is_loaded(self) -> bool:
        """Check if real image is loaded."""
        return self._real_image is not None
```

### Usage

```python
# Virtual Proxy - lazy loading
image = ImageProxy("large_photo.jpg")
print(image.is_loaded())  # False - not loaded yet
print(image.display())  # Now loaded and displayed
print(image.is_loaded())  # True - already loaded
```

## Trade-offs

**Benefits:**

1. Controls access to real object
2. Defers expensive operations until needed (lazy initialization)
3. Implements authentication and authorization for access control
4. Adds behavior without modifying real object

**Drawbacks:**

1. Adds additional classes and indirection increasing complexity
2. Proxy adds overhead affecting performance
3. Lazy initialization may cause delays in response time
4. Thread-safe proxies can be complex

## Real-World Examples

- ORM frameworks with database proxy objects for lazy loading
- Virtual images as placeholders in documents
- Network proxies like HTTP proxies, SOCKS proxies
- Security proxies for authentication and authorization layers

## Related Patterns

- Adapter
- Decorator
- Facade

## API Reference

::: design_patterns.structural.proxy
    options:
      show_root_heading: true
      show_source: true
