# Iterator Pattern

**Category:** Behavioral Pattern

## Overview

Provide a way to access elements of an aggregate object sequentially without exposing its underlying representation. This pattern decouples the traversal logic from the collection, allowing different traversal algorithms while keeping the collection interface simple.

## Usage Guidelines

**Use when:**
- Need to access collection elements sequentially
- Want different ways to traverse same collection
- Want uniform interface for traversing different collections
- Internal collection structure should be hidden

**Avoid when:**
- Built-in iteration is sufficient for simple collections
- Need random access to elements
- Only one way to traverse collection exists
- Python's built-in iteration protocol works well

## Implementation

```python
from __future__ import annotations
from typing import Iterator as TypingIterator

class Book:
    """Represents a book in the library."""

    def __init__(self, title: str, author: str) -> None:
        """Initialize a book."""
        self.title = title
        self.author = author

    def __str__(self) -> str:
        """String representation of the book."""
        return f"{self.title} by {self.author}"

class BookIterator:
    """Concrete iterator for books."""

    def __init__(self, books: list[Book]) -> None:
        """Initialize the iterator."""
        self._books = books
        self._index = 0

    def has_next(self) -> bool:
        """Check if more books exist."""
        return self._index < len(self._books)

    def next(self) -> Book:
        """Get next book."""
        if not self.has_next():
            raise StopIteration("No more books")

        book = self._books[self._index]
        self._index += 1
        return book

class BookCollection:
    """Concrete aggregate of books implementing Python iterator protocol."""

    def __init__(self) -> None:
        """Initialize an empty book collection."""
        self._books: list[Book] = []

    def add_book(self, book: Book) -> None:
        """Add a book to the collection."""
        self._books.append(book)

    def create_iterator(self) -> BookIterator:
        """Create an iterator for this collection."""
        return BookIterator(self._books)

    def __iter__(self) -> TypingIterator[Book]:
        """Make collection iterable using Python's iterator protocol."""
        return iter(self._books)

    def __len__(self) -> int:
        """Get collection length."""
        return len(self._books)
```

### Usage

```python
# Book collection with Python's iterator protocol
library = BookCollection()
library.add_book(Book("Design Patterns", "Gang of Four"))
library.add_book(Book("Clean Code", "Robert Martin"))
library.add_book(Book("Refactoring", "Martin Fowler"))

# Using Python's for loop
for book in library:
    print(book)
# Output:
# Design Patterns by Gang of Four
# Clean Code by Robert Martin
# Refactoring by Martin Fowler

# Using custom iterator
iterator = library.create_iterator()
while iterator.has_next():
    book = iterator.next()
    print(book.title)
```

## Trade-offs

**Benefits:**
1. Separates traversal logic from collection (Single Responsibility Principle)
2. Multiple traversals can happen simultaneously
3. Same interface for different collections provides uniformity
4. Collection internals remain hidden through encapsulation

**Drawbacks:**
1. Overkill for simple collections
2. Additional abstraction adds performance overhead
3. Iterator must track traversal state
4. Modifying collection during iteration can cause problems

## Real-World Examples

- Database result sets iterating through query results
- File systems traversing directories and files
- DOM traversal walking through HTML/XML trees
- Graph traversal with BFS, DFS algorithms

## Related Patterns

- Composite
- Factory Method
- Memento
- Visitor

## API Reference

::: design_patterns.behavioral.iterator
    options:
      show_root_heading: true
      show_source: true
