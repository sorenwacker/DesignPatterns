"""Tests for the Iterator pattern."""

import pytest
from design_patterns.behavioral.iterator import (
    BinaryTree,
    Book,
    BookCollection,
    Range,
)


def test_book_collection_add():
    """Test adding books to collection."""
    collection = BookCollection()
    book = Book("Design Patterns", "GoF")

    collection.add_book(book)
    assert collection.size() == 1


def test_book_collection_remove():
    """Test removing books from collection."""
    collection = BookCollection()
    book = Book("Clean Code", "Robert Martin")

    collection.add_book(book)
    collection.remove_book(book)
    assert collection.size() == 0


def test_book_iterator_has_next():
    """Test iterator has_next method."""
    collection = BookCollection()
    collection.add_book(Book("Book 1", "Author 1"))
    collection.add_book(Book("Book 2", "Author 2"))

    iterator = collection.create_iterator()
    assert iterator.has_next() is True


def test_book_iterator_next():
    """Test iterator next method."""
    collection = BookCollection()
    book1 = Book("Book 1", "Author 1")
    book2 = Book("Book 2", "Author 2")

    collection.add_book(book1)
    collection.add_book(book2)

    iterator = collection.create_iterator()
    assert iterator.next() == book1
    assert iterator.next() == book2


def test_book_iterator_exhaustion():
    """Test iterator raises StopIteration when exhausted."""
    collection = BookCollection()
    collection.add_book(Book("Book 1", "Author 1"))

    iterator = collection.create_iterator()
    iterator.next()

    with pytest.raises(StopIteration, match="No more books"):
        iterator.next()


def test_book_collection_python_iterator():
    """Test Python iterator protocol support."""
    collection = BookCollection()
    collection.add_book(Book("Book 1", "Author 1"))
    collection.add_book(Book("Book 2", "Author 2"))
    collection.add_book(Book("Book 3", "Author 3"))

    books = list(collection)
    assert len(books) == 3
    assert books[0].title == "Book 1"


def test_book_collection_for_loop():
    """Test iterating with for loop."""
    collection = BookCollection()
    collection.add_book(Book("Book 1", "Author 1"))
    collection.add_book(Book("Book 2", "Author 2"))

    titles = []
    for book in collection:
        titles.append(book.title)

    assert titles == ["Book 1", "Book 2"]


def test_book_str_representation():
    """Test book string representation."""
    book = Book("Design Patterns", "GoF")
    assert str(book) == "Design Patterns by GoF"


def test_binary_tree_insert():
    """Test inserting values into binary tree."""
    tree = BinaryTree()
    tree.insert(5)
    tree.insert(3)
    tree.insert(7)

    assert tree.root.value == 5
    assert tree.root.left.value == 3
    assert tree.root.right.value == 7


def test_binary_tree_in_order_traversal():
    """Test in-order iterator on binary tree."""
    tree = BinaryTree()
    tree.insert(5)
    tree.insert(3)
    tree.insert(7)
    tree.insert(1)
    tree.insert(9)

    iterator = tree.create_iterator()
    values = []

    while iterator.has_next():
        values.append(iterator.next())

    assert values == [1, 3, 5, 7, 9]


def test_binary_tree_iterator_exhaustion():
    """Test tree iterator raises StopIteration when exhausted."""
    tree = BinaryTree()
    tree.insert(5)

    iterator = tree.create_iterator()
    iterator.next()

    with pytest.raises(StopIteration, match="No more nodes"):
        iterator.next()


def test_empty_tree_iterator():
    """Test iterator on empty tree."""
    tree = BinaryTree()
    iterator = tree.create_iterator()

    assert iterator.has_next() is False


def test_custom_range():
    """Test custom Range implementation."""
    r = Range(0, 5)
    values = list(r)

    assert values == [0, 1, 2, 3, 4]


def test_custom_range_with_step():
    """Test Range with custom step."""
    r = Range(0, 10, 2)
    values = list(r)

    assert values == [0, 2, 4, 6, 8]


def test_custom_range_length():
    """Test Range length calculation."""
    r = Range(0, 10, 2)
    assert len(r) == 5


def test_custom_range_empty():
    """Test empty Range."""
    r = Range(5, 5)
    values = list(r)

    assert values == []
    assert len(r) == 0


def test_book_collection_get():
    """Test getting book by index."""
    collection = BookCollection()
    book1 = Book("Book 1", "Author 1")
    book2 = Book("Book 2", "Author 2")

    collection.add_book(book1)
    collection.add_book(book2)

    assert collection.get_book(0) == book1
    assert collection.get_book(1) == book2


def test_book_collection_len():
    """Test collection length via __len__."""
    collection = BookCollection()
    collection.add_book(Book("Book 1", "Author 1"))
    collection.add_book(Book("Book 2", "Author 2"))

    assert len(collection) == 2


def test_multiple_iterators():
    """Test that multiple iterators can coexist."""
    collection = BookCollection()
    collection.add_book(Book("Book 1", "Author 1"))
    collection.add_book(Book("Book 2", "Author 2"))

    iter1 = collection.create_iterator()
    iter2 = collection.create_iterator()

    assert iter1.next().title == "Book 1"
    assert iter2.next().title == "Book 1"
    assert iter1.next().title == "Book 2"
