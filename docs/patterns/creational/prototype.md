# Prototype Pattern

**Category:** Creational Pattern

## Overview

Create new objects by cloning existing instances rather than creating new ones from scratch. This pattern is useful when object creation is expensive or when you want to avoid the complexity of instantiating an object directly, leveraging Python's built-in `copy` module for shallow and deep copying.

## Usage Guidelines

**Use when:**

- Creating new objects is more expensive than cloning existing ones
- Objects require complex setup that can be reused
- Types to create are determined at runtime
- Need copies of objects in specific states

**Avoid when:**

- Creating new objects is straightforward and cheap
- Complexity of managing object references outweighs benefits
- Objects contain circular references that complicate cloning
- Objects are immutable and can be safely shared

## Implementation

```python
from __future__ import annotations
import copy
from typing import Any

class Prototype:
    """Abstract base class for prototypes.

    Defines the interface for cloning objects.
    """

    def clone(self) -> Prototype:
        """Create a shallow copy of the object.

        Returns:
            A shallow copy of the prototype.
        """
        return copy.copy(self)

    def deep_clone(self) -> Prototype:
        """Create a deep copy of the object.

        Returns:
            A deep copy of the prototype.
        """
        return copy.deepcopy(self)

class Document(Prototype):
    """Represents a document that can be cloned.

    This demonstrates the prototype pattern with both shallow and deep copying.
    """

    def __init__(self, title: str, font: str, font_size: int) -> None:
        """Initialize a document.

        Args:
            title: The document title.
            font: The font name.
            font_size: The font size.
        """
        self.title = title
        self.font = font
        self.font_size = font_size
        self.sections: list[str] = []
        self.metadata: dict[str, Any] = {}

    def add_section(self, section: str) -> None:
        """Add a section to the document.

        Args:
            section: The section name or content.
        """
        self.sections.append(section)

    def set_metadata(self, key: str, value: Any) -> None:
        """Set document metadata.

        Args:
            key: The metadata key.
            value: The metadata value.
        """
        self.metadata[key] = value

    def get_info(self) -> str:
        """Get document information.

        Returns:
            A string describing the document.
        """
        return (f"Document: {self.title}, "
                f"Font: {self.font} {self.font_size}pt, "
                f"Sections: {len(self.sections)}")
```

### Usage

```python
# Create original document
original = Document("Report", "Arial", 12)
original.add_section("Introduction")
original.add_section("Methodology")
original.set_metadata("author", "John Doe")

# Shallow copy - shares mutable references
shallow_copy = original.clone()
shallow_copy.title = "Modified Report"
shallow_copy.add_section("Results")  # Affects original too!

# Deep copy - independent copy
deep_copy = original.deep_clone()
deep_copy.title = "Independent Report"
deep_copy.add_section("Conclusion")  # Does NOT affect original

print(f"Original sections: {len(original.sections)}")  # 3
print(f"Deep copy sections: {len(deep_copy.sections)}")  # 4
```

## Trade-offs

**Benefits:**

1. Cloning can be faster than creating objects from scratch
2. Add or remove prototypes at runtime for flexibility
3. Avoid factory hierarchies for product variants
4. Clone objects in specific configured states

**Drawbacks:**

1. Managing shallow vs deep copy semantics can be tricky
2. Objects with circular references are hard to clone
3. Implementing proper cloning can be complex
4. Cloned objects may need additional initialization

## Real-World Examples

- Document templates with pre-configured settings
- Game objects with preset configurations (enemies, weapons, items)
- Graphics editors cloning shapes or design elements
- Test fixtures cloning test data objects

## Related Patterns

- Abstract Factory
- Composite
- Decorator
- Memento
- Singleton

## API Reference

::: design_patterns.creational.prototype
    options:
      show_root_heading: true
      show_source: true
