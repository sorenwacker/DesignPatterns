"""Iterator Pattern Module

The Iterator pattern provides a way to access elements of an aggregate object
sequentially without exposing its underlying representation. It decouples the
traversal logic from the collection, allowing different traversal algorithms.

Example:
    Iterating through a custom collection:

    ```python
    library = BookCollection()
    library.add_book(Book("Design Patterns", "GoF"))
    library.add_book(Book("Clean Code", "Robert Martin"))

    for book in library:
        print(book.title)
    ```
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Iterator as TypingIterator


class Iterator(ABC):
    """Abstract iterator interface."""

    @abstractmethod
    def has_next(self) -> bool:
        """Check if there are more elements.

        Returns:
            True if more elements exist.
        """
        pass

    @abstractmethod
    def next(self) -> Any:
        """Get the next element.

        Returns:
            The next element.

        Raises:
            StopIteration: When no more elements exist.
        """
        pass


class Aggregate(ABC):
    """Abstract aggregate interface."""

    @abstractmethod
    def create_iterator(self) -> Iterator:
        """Create an iterator for this aggregate.

        Returns:
            An iterator instance.
        """
        pass


class Book:
    """Represents a book in the library."""

    def __init__(self, title: str, author: str) -> None:
        """Initialize a book.

        Args:
            title: Book title.
            author: Book author.
        """
        self.title = title
        self.author = author

    def __str__(self) -> str:
        """String representation of the book.

        Returns:
            Book details.
        """
        return f"{self.title} by {self.author}"


class BookIterator(Iterator):
    """Concrete iterator for books."""

    def __init__(self, books: list[Book]) -> None:
        """Initialize the iterator.

        Args:
            books: List of books to iterate.
        """
        self._books = books
        self._index = 0

    def has_next(self) -> bool:
        """Check if more books exist.

        Returns:
            True if more books exist.
        """
        return self._index < len(self._books)

    def next(self) -> Book:
        """Get next book.

        Returns:
            The next book.

        Raises:
            StopIteration: When no more books exist.
        """
        if not self.has_next():
            raise StopIteration("No more books")

        book = self._books[self._index]
        self._index += 1
        return book


class BookCollection(Aggregate):
    """Concrete aggregate of books implementing Python iterator protocol."""

    def __init__(self) -> None:
        """Initialize an empty book collection."""
        self._books: list[Book] = []

    def add_book(self, book: Book) -> None:
        """Add a book to the collection.

        Args:
            book: Book to add.
        """
        self._books.append(book)

    def remove_book(self, book: Book) -> None:
        """Remove a book from the collection.

        Args:
            book: Book to remove.
        """
        if book in self._books:
            self._books.remove(book)

    def get_book(self, index: int) -> Book:
        """Get book at index.

        Args:
            index: Book index.

        Returns:
            Book at the specified index.
        """
        return self._books[index]

    def size(self) -> int:
        """Get number of books.

        Returns:
            Number of books in collection.
        """
        return len(self._books)

    def create_iterator(self) -> BookIterator:
        """Create an iterator for this collection.

        Returns:
            Book iterator.
        """
        return BookIterator(self._books)

    def __iter__(self) -> TypingIterator[Book]:
        """Make collection iterable using Python's iterator protocol.

        Returns:
            Iterator over books.
        """
        return iter(self._books)

    def __len__(self) -> int:
        """Get collection length.

        Returns:
            Number of books.
        """
        return len(self._books)


class TreeNode:
    """Node in a binary tree."""

    def __init__(self, value: int) -> None:
        """Initialize a tree node.

        Args:
            value: Node value.
        """
        self.value = value
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None


class InOrderIterator(Iterator):
    """Iterator for in-order tree traversal."""

    def __init__(self, root: TreeNode | None) -> None:
        """Initialize in-order iterator.

        Args:
            root: Root of the tree.
        """
        self._stack: list[TreeNode] = []
        self._current = root
        self._push_left_nodes(root)

    def _push_left_nodes(self, node: TreeNode | None) -> None:
        """Push all left nodes onto stack.

        Args:
            node: Starting node.
        """
        while node:
            self._stack.append(node)
            node = node.left

    def has_next(self) -> bool:
        """Check if more nodes exist.

        Returns:
            True if more nodes exist.
        """
        return len(self._stack) > 0

    def next(self) -> int:
        """Get next node value in in-order traversal.

        Returns:
            Next node value.

        Raises:
            StopIteration: When no more nodes exist.
        """
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
        """Insert a value into the tree.

        Args:
            value: Value to insert.
        """
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node: TreeNode, value: int) -> None:
        """Recursively insert value.

        Args:
            node: Current node.
            value: Value to insert.
        """
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
        """Create an in-order iterator.

        Returns:
            In-order iterator.
        """
        return InOrderIterator(self.root)


class Range:
    """Custom range implementation demonstrating iterator pattern."""

    def __init__(self, start: int, end: int, step: int = 1) -> None:
        """Initialize range.

        Args:
            start: Start value.
            end: End value (exclusive).
            step: Step size.
        """
        self.start = start
        self.end = end
        self.step = step

    def __iter__(self) -> TypingIterator[int]:
        """Create iterator for the range.

        Returns:
            Range iterator.
        """
        current = self.start
        while current < self.end:
            yield current
            current += self.step

    def __len__(self) -> int:
        """Calculate range length.

        Returns:
            Number of elements in range.
        """
        return max(0, (self.end - self.start + self.step - 1) // self.step)
