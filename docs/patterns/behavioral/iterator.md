# Iterator Pattern

**Category:** Behavioral Pattern

## Intent

Provide a way to access elements of an aggregate object sequentially without exposing its underlying representation. The Iterator pattern decouples the traversal logic from the collection, allowing different traversal algorithms while keeping the collection interface simple.

## Problem

When you need to traverse collections, direct access to internal structure leads to:

- Exposing internal representation of collections
- Multiple traversal methods cluttering collection interface
- Difficulty implementing different traversal algorithms
- Client code coupled to collection structure
- Violation of single responsibility principle

## When to Use

Use the Iterator pattern when:

- **Sequential access**: Need to access collection elements sequentially
- **Multiple traversals**: Want different ways to traverse same collection
- **Uniform interface**: Want uniform interface for traversing different collections
- **Hide representation**: Internal collection structure should be hidden
- **Simplified collection**: Collection interface should focus on storage, not traversal
- **Composite structures**: Traversing tree or graph structures

## When NOT to Use

Avoid the Iterator pattern when:

- **Simple collections**: Built-in iteration is sufficient
- **Random access**: Need random access to elements
- **Single traversal**: Only one way to traverse collection
- **Direct access**: Direct indexing is more appropriate
- **Python iteration**: Python's built-in iteration protocol works well

## Structure

The Iterator pattern involves:

- **Iterator**: Interface for accessing and traversing elements
- **Concrete Iterator**: Implements iterator interface for specific collection
- **Aggregate**: Interface for creating iterator
- **Concrete Aggregate**: Implements aggregate and returns concrete iterator

## Implementation

### Book Collection Example

```python
from __future__ import annotations
from abc import ABC, abstractmethod
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

    def remove_book(self, book: Book) -> None:
        """Remove a book from the collection."""
        if book in self._books:
            self._books.remove(book)

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

### Binary Tree Iterator Example

```python
class TreeNode:
    """Node in a binary tree."""

    def __init__(self, value: int) -> None:
        """Initialize a tree node."""
        self.value = value
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None

class InOrderIterator:
    """Iterator for in-order tree traversal."""

    def __init__(self, root: TreeNode | None) -> None:
        """Initialize in-order iterator."""
        self._stack: list[TreeNode] = []
        self._current = root
        self._push_left_nodes(root)

    def _push_left_nodes(self, node: TreeNode | None) -> None:
        """Push all left nodes onto stack."""
        while node:
            self._stack.append(node)
            node = node.left

    def has_next(self) -> bool:
        """Check if more nodes exist."""
        return len(self._stack) > 0

    def next(self) -> int:
        """Get next node value in in-order traversal."""
        if not self.has_next():
            raise StopIteration("No more nodes")

        node = self._stack.pop()
        value = node.value

        if node.right:
            self._push_left_nodes(node.right)

        return value

class BinaryTree:
    """Binary tree with custom iterator."""

    def __init__(self) -> None:
        """Initialize an empty binary tree."""
        self.root: TreeNode | None = None

    def insert(self, value: int) -> None:
        """Insert a value into the tree."""
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node: TreeNode, value: int) -> None:
        """Recursively insert value."""
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)

    def create_iterator(self) -> InOrderIterator:
        """Create an in-order iterator."""
        return InOrderIterator(self.root)
```

## Usage Example

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

# Binary tree traversal
tree = BinaryTree()
tree.insert(5)
tree.insert(3)
tree.insert(7)
tree.insert(1)
tree.insert(9)

# In-order traversal: 1, 3, 5, 7, 9
iterator = tree.create_iterator()
values = []
while iterator.has_next():
    values.append(iterator.next())
print(values)  # [1, 3, 5, 7, 9]
```

## Key Benefits

1. **Single Responsibility**: Separates traversal logic from collection
2. **Multiple iterators**: Multiple traversals can happen simultaneously
3. **Uniform interface**: Same interface for different collections
4. **Different algorithms**: Easy to implement different traversal algorithms
5. **Encapsulation**: Collection internals remain hidden
6. **Simplified collection**: Collection interface focuses on storage

## Drawbacks

1. **Overkill**: Simple collections don't need iterators
2. **Performance**: Additional abstraction adds overhead
3. **State management**: Iterator must track traversal state
4. **Modification issues**: Modifying collection during iteration can cause problems
5. **Memory**: Multiple iterators consume memory

## Real-World Examples

- **Database result sets**: Iterating through query results
- **File systems**: Traversing directories and files
- **Collections**: Lists, sets, maps in programming languages
- **DOM traversal**: Walking through HTML/XML document trees
- **Graph traversal**: BFS, DFS traversals
- **Streams**: Reading data from input streams
- **Pagination**: Iterating through paginated results

## Related Patterns

- **Composite**: Iterators often used to traverse composites
- **Factory Method**: Can create different iterator types
- **Memento**: Can store iterator state for restoration
- **Visitor**: Visitor traverses structure, Iterator provides access

## API Reference

::: design_patterns.behavioral.iterator
    options:
      show_root_heading: true
      show_source: true
