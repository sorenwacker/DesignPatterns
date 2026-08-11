"""Proxy Pattern Module

The Proxy pattern provides a surrogate or placeholder for another object to control
access to it. There are several types of proxies:
- Virtual Proxy: Controls access to expensive-to-create objects
- Protection Proxy: Controls access based on permissions
- Remote Proxy: Represents an object in a different address space
- Caching Proxy: Caches results of expensive operations

Example:
    Using a virtual proxy for lazy loading:

    ```python
    image = ImageProxy("large_photo.jpg")
    # Image not loaded yet

    image.display()  # Now image is loaded and displayed
    image.display()  # Uses cached image, no reload
    ```
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Image(ABC):
    """Abstract interface for images."""

    @abstractmethod
    def display(self) -> str:
        """Display the image.

        Returns:
            Display message.
        """

    @abstractmethod
    def get_filename(self) -> str:
        """Get the image filename.

        Returns:
            Filename string.
        """


class RealImage(Image):
    """Real image that is expensive to load."""

    def __init__(self, filename: str) -> None:
        """Initialize and load the image.

        Args:
            filename: Image filename.
        """
        self.filename = filename
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        """Simulate expensive loading operation."""

    def display(self) -> str:
        """Display the image.

        Returns:
            Display message.
        """
        return f"Displaying {self.filename}"

    def get_filename(self) -> str:
        """Get filename.

        Returns:
            Filename.
        """
        return self.filename


class ImageProxy(Image):
    """Virtual proxy for lazy loading images."""

    def __init__(self, filename: str) -> None:
        """Initialize proxy without loading image.

        Args:
            filename: Image filename.
        """
        self.filename = filename
        self._real_image: RealImage | None = None

    def display(self) -> str:
        """Display image, loading it if necessary.

        Returns:
            Display message.
        """
        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        return self._real_image.display()

    def get_filename(self) -> str:
        """Get filename without loading image.

        Returns:
            Filename.
        """
        return self.filename

    def is_loaded(self) -> bool:
        """Check if real image is loaded.

        Returns:
            True if loaded, False otherwise.
        """
        return self._real_image is not None


class Internet(ABC):
    """Abstract interface for internet access."""

    @abstractmethod
    def connect(self, url: str) -> str:
        """Connect to a URL.

        Args:
            url: URL to connect to.

        Returns:
            Connection result.
        """


class RealInternet(Internet):
    """Real internet connection."""

    def connect(self, url: str) -> str:
        """Connect to URL.

        Args:
            url: URL to connect to.

        Returns:
            Connection success message.
        """
        return f"Connected to {url}"


class ProxyInternet(Internet):
    """Protection proxy that filters internet access."""

    def __init__(self) -> None:
        """Initialize proxy with real internet and banned sites."""
        self._real_internet = RealInternet()
        self._banned_sites = ["banned.com", "restricted.net", "blocked.org"]

    def connect(self, url: str) -> str:
        """Connect to URL if not banned.

        Args:
            url: URL to connect to.

        Returns:
            Connection result or blocked message.
        """
        for banned in self._banned_sites:
            if banned in url:
                return f"Access denied to {url}"
        return self._real_internet.connect(url)

    def add_banned_site(self, site: str) -> None:
        """Add a site to the banned list.

        Args:
            site: Site to ban.
        """
        if site not in self._banned_sites:
            self._banned_sites.append(site)


class Database(ABC):
    """Abstract interface for database."""

    @abstractmethod
    def query(self, sql: str) -> str:
        """Execute a query.

        Args:
            sql: SQL query.

        Returns:
            Query result.
        """


class RealDatabase(Database):
    """Real database implementation."""

    def query(self, sql: str) -> str:
        """Execute query on real database.

        Args:
            sql: SQL query.

        Returns:
            Query result.
        """
        return f"Executed: {sql}"


class DatabaseProxy(Database):
    """Caching proxy for database queries."""

    def __init__(self) -> None:
        """Initialize proxy with real database and cache."""
        self._real_database = RealDatabase()
        self._cache: dict[str, str] = {}

    def query(self, sql: str) -> str:
        """Execute query with caching.

        Args:
            sql: SQL query.

        Returns:
            Cached or fresh query result.
        """
        if sql in self._cache:
            return f"Cached: {self._cache[sql]}"

        result = self._real_database.query(sql)
        self._cache[sql] = result
        return result

    def clear_cache(self) -> None:
        """Clear the query cache."""
        self._cache.clear()

    def get_cache_size(self) -> int:
        """Get number of cached queries.

        Returns:
            Cache size.
        """
        return len(self._cache)


class Document(ABC):
    """Abstract interface for documents."""

    @abstractmethod
    def read(self) -> str:
        """Read the document.

        Returns:
            Document content.
        """

    @abstractmethod
    def write(self, content: str) -> str:
        """Write to the document.

        Args:
            content: Content to write.

        Returns:
            Write result.
        """


class RealDocument(Document):
    """Real document implementation."""

    def __init__(self, filename: str) -> None:
        """Initialize document.

        Args:
            filename: Document filename.
        """
        self.filename = filename
        self._content = ""

    def read(self) -> str:
        """Read document content.

        Returns:
            Document content.
        """
        return f"Reading {self.filename}: {self._content}"

    def write(self, content: str) -> str:
        """Write content to document.

        Args:
            content: Content to write.

        Returns:
            Write confirmation.
        """
        self._content = content
        return f"Written to {self.filename}"


class ProtectedDocumentProxy(Document):
    """Protection proxy that requires authentication."""

    def __init__(self, filename: str, user_role: str) -> None:
        """Initialize protected document proxy.

        Args:
            filename: Document filename.
            user_role: User's role (admin or user).
        """
        self._real_document = RealDocument(filename)
        self.user_role = user_role

    def read(self) -> str:
        """Read document (allowed for all users).

        Returns:
            Document content.
        """
        return self._real_document.read()

    def write(self, content: str) -> str:
        """Write to document (requires admin role).

        Args:
            content: Content to write.

        Returns:
            Write result or access denied message.
        """
        if self.user_role == "admin":
            return self._real_document.write(content)
        return "Access denied: admin role required for writing"
