# Proxy Pattern

**Category:** Structural Pattern

## Intent

Provide a surrogate or placeholder for another object to control access to it. The Proxy pattern is used to create a representative object that controls access to another object, which may be remote, expensive to create, or require protection. There are several types of proxies: Virtual Proxy (lazy loading), Protection Proxy (access control), Remote Proxy (remote objects), and Caching Proxy (cache results).

## Problem

When direct access to objects is problematic, it leads to:

- Expensive object creation affecting performance
- No access control to sensitive objects
- Difficulty adding behavior without modifying original class
- Complex remote object access
- No caching of expensive operations

## When to Use

Use the Proxy pattern when:

- **Lazy initialization**: Defer expensive object creation until needed
- **Access control**: Control access based on permissions or authentication
- **Remote objects**: Access objects in different address spaces
- **Logging**: Log access to objects
- **Caching**: Cache results of expensive operations
- **Reference counting**: Track object usage
- **Smart references**: Add behavior when accessing objects

## When NOT to Use

Avoid the Proxy pattern when:

- **Simple access**: Direct access is sufficient
- **No control needed**: No access control or lazy loading required
- **Performance overhead**: Proxy overhead is unacceptable
- **Overkill**: Pattern adds unnecessary complexity
- **Direct modification**: Can modify original class directly

## Structure

The Proxy pattern involves:

- **Subject**: Interface for both real object and proxy
- **Real Subject**: Real object that proxy represents
- **Proxy**: Controls access to real subject
- **Client**: Works with subject through proxy

## Implementation

### Virtual Proxy (Lazy Loading)

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

### Protection Proxy (Access Control)

```python
class Internet(ABC):
    """Abstract interface for internet access."""

    @abstractmethod
    def connect(self, url: str) -> str:
        """Connect to a URL."""
        pass

class RealInternet(Internet):
    """Real internet connection."""

    def connect(self, url: str) -> str:
        """Connect to URL."""
        return f"Connected to {url}"

class ProxyInternet(Internet):
    """Protection proxy that filters internet access."""

    def __init__(self) -> None:
        """Initialize proxy with real internet and banned sites."""
        self._real_internet = RealInternet()
        self._banned_sites = ["banned.com", "restricted.net", "blocked.org"]

    def connect(self, url: str) -> str:
        """Connect to URL if not banned."""
        for banned in self._banned_sites:
            if banned in url:
                return f"Access denied to {url}"
        return self._real_internet.connect(url)

    def add_banned_site(self, site: str) -> None:
        """Add a site to the banned list."""
        if site not in self._banned_sites:
            self._banned_sites.append(site)
```

### Caching Proxy

```python
class Database(ABC):
    """Abstract interface for database."""

    @abstractmethod
    def query(self, sql: str) -> str:
        """Execute a query."""
        pass

class RealDatabase(Database):
    """Real database implementation."""

    def query(self, sql: str) -> str:
        """Execute query on real database."""
        return f"Executed: {sql}"

class DatabaseProxy(Database):
    """Caching proxy for database queries."""

    def __init__(self) -> None:
        """Initialize proxy with real database and cache."""
        self._real_database = RealDatabase()
        self._cache: dict[str, str] = {}

    def query(self, sql: str) -> str:
        """Execute query with caching."""
        if sql in self._cache:
            return f"Cached: {self._cache[sql]}"

        result = self._real_database.query(sql)
        self._cache[sql] = result
        return result

    def clear_cache(self) -> None:
        """Clear the query cache."""
        self._cache.clear()

    def get_cache_size(self) -> int:
        """Get number of cached queries."""
        return len(self._cache)
```

### Protection Proxy with Roles

```python
class Document(ABC):
    """Abstract interface for documents."""

    @abstractmethod
    def read(self) -> str:
        """Read the document."""
        pass

    @abstractmethod
    def write(self, content: str) -> str:
        """Write to the document."""
        pass

class RealDocument(Document):
    """Real document implementation."""

    def __init__(self, filename: str) -> None:
        """Initialize document."""
        self.filename = filename
        self._content = ""

    def read(self) -> str:
        """Read document content."""
        return f"Reading {self.filename}: {self._content}"

    def write(self, content: str) -> str:
        """Write content to document."""
        self._content = content
        return f"Written to {self.filename}"

class ProtectedDocumentProxy(Document):
    """Protection proxy that requires authentication."""

    def __init__(self, filename: str, user_role: str) -> None:
        """Initialize protected document proxy."""
        self._real_document = RealDocument(filename)
        self.user_role = user_role

    def read(self) -> str:
        """Read document (allowed for all users)."""
        return self._real_document.read()

    def write(self, content: str) -> str:
        """Write to document (requires admin role)."""
        if self.user_role == "admin":
            return self._real_document.write(content)
        return "Access denied: admin role required for writing"
```

## Usage Example

```python
# Virtual Proxy - lazy loading
image = ImageProxy("large_photo.jpg")
print(image.is_loaded())  # False - not loaded yet
print(image.display())  # Now loaded and displayed
print(image.is_loaded())  # True - already loaded

# Protection Proxy - access control
internet = ProxyInternet()
print(internet.connect("www.google.com"))  # Connected to www.google.com
print(internet.connect("www.banned.com"))  # Access denied to www.banned.com

internet.add_banned_site("facebook.com")
print(internet.connect("www.facebook.com"))  # Access denied to www.facebook.com

# Caching Proxy
db = DatabaseProxy()
print(db.query("SELECT * FROM users"))  # Executed: SELECT * FROM users
print(db.query("SELECT * FROM users"))  # Cached: Executed: SELECT * FROM users
print(f"Cache size: {db.get_cache_size()}")  # Cache size: 1

# Protected Document
admin_doc = ProtectedDocumentProxy("secret.txt", "admin")
print(admin_doc.write("Confidential"))  # Written to secret.txt
print(admin_doc.read())  # Reading secret.txt: Confidential

user_doc = ProtectedDocumentProxy("secret.txt", "user")
print(user_doc.read())  # Reading secret.txt: Confidential
print(user_doc.write("Try to write"))  # Access denied: admin role required for writing
```

## Key Benefits

1. **Controlled access**: Controls access to real object
2. **Lazy initialization**: Defers expensive operations until needed
3. **Access control**: Implements authentication and authorization
4. **Additional behavior**: Adds behavior without modifying real object
5. **Remote access**: Simplifies access to remote objects
6. **Caching**: Improves performance through caching
7. **Logging**: Can log all access to objects

## Drawbacks

1. **Complexity**: Adds additional classes and indirection
2. **Performance**: Proxy adds overhead
3. **Response time**: Lazy initialization may cause delays
4. **Maintenance**: More classes to maintain
5. **Synchronization**: Thread-safe proxies can be complex

## Real-World Examples

- **ORM frameworks**: Database proxy objects (lazy loading)
- **Virtual images**: Image placeholders in documents
- **Network proxies**: HTTP proxies, SOCKS proxies
- **Security proxies**: Authentication and authorization layers
- **Smart pointers**: C++ smart pointers controlling object lifetime
- **Caching layers**: Redis, Memcached as caching proxies
- **Remote objects**: RMI, CORBA proxy objects
- **Copy-on-write**: File system and memory management

## Related Patterns

- **Adapter**: Changes interface, Proxy keeps same interface
- **Decorator**: Adds behavior, Proxy controls access
- **Facade**: Simplifies interface, Proxy controls access

## API Reference

::: design_patterns.structural.proxy
    options:
      show_root_heading: true
      show_source: true
