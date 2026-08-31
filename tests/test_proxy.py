"""Tests for the Proxy pattern."""

from design_patterns.structural.proxy import (
    DatabaseProxy,
    ImageProxy,
    ProtectedDocumentProxy,
    ProxyInternet,
    RealImage,
)


def test_real_image_display():
    """Test real image display."""
    image = RealImage("photo.jpg")
    result = image.display()

    assert result == "Displaying photo.jpg"
    assert image.get_filename() == "photo.jpg"


def test_image_proxy_lazy_loading():
    """Test that image proxy delays loading."""
    proxy = ImageProxy("large_photo.jpg")

    assert proxy.is_loaded() is False
    assert proxy.get_filename() == "large_photo.jpg"

    result = proxy.display()
    assert "large_photo.jpg" in result
    assert proxy.is_loaded() is True


def test_image_proxy_caches_real_image():
    """Test that proxy caches the real image."""
    proxy = ImageProxy("photo.jpg")

    proxy.display()
    assert proxy.is_loaded() is True

    # Second display should use cached image
    result = proxy.display()
    assert "photo.jpg" in result


def test_proxy_internet_allows_normal_sites():
    """Test that proxy allows access to normal sites."""
    internet = ProxyInternet()

    result = internet.connect("google.com")
    assert result == "Connected to google.com"

    result = internet.connect("github.com")
    assert result == "Connected to github.com"


def test_proxy_internet_blocks_banned_sites():
    """Test that proxy blocks banned sites."""
    internet = ProxyInternet()

    result = internet.connect("banned.com")
    assert "Access denied" in result

    result = internet.connect("restricted.net")
    assert "Access denied" in result


def test_proxy_internet_add_banned_site():
    """Test adding sites to ban list."""
    internet = ProxyInternet()

    result = internet.connect("newsite.com")
    assert "Connected" in result

    internet.add_banned_site("newsite.com")
    result = internet.connect("newsite.com")
    assert "Access denied" in result


def test_database_proxy_caching():
    """Test that database proxy caches queries."""
    db = DatabaseProxy()

    result1 = db.query("SELECT * FROM users")
    assert "Executed: SELECT * FROM users" in result1

    result2 = db.query("SELECT * FROM users")
    assert "Cached:" in result2


def test_database_proxy_different_queries():
    """Test that different queries are cached separately."""
    db = DatabaseProxy()

    db.query("SELECT * FROM users")
    db.query("SELECT * FROM products")

    assert db.get_cache_size() == 2


def test_database_proxy_clear_cache():
    """Test clearing database cache."""
    db = DatabaseProxy()

    db.query("SELECT * FROM users")
    assert db.get_cache_size() == 1

    db.clear_cache()
    assert db.get_cache_size() == 0


def test_database_proxy_after_cache_clear():
    """Test querying after cache clear executes on real database."""
    db = DatabaseProxy()

    db.query("SELECT * FROM users")
    db.clear_cache()

    result = db.query("SELECT * FROM users")
    assert "Executed:" in result
    assert "Cached:" not in result


def test_protected_document_read():
    """Test that all users can read documents."""
    admin_doc = ProtectedDocumentProxy("report.txt", "admin")
    user_doc = ProtectedDocumentProxy("report.txt", "user")

    admin_result = admin_doc.read()
    user_result = user_doc.read()

    assert "Reading report.txt" in admin_result
    assert "Reading report.txt" in user_result


def test_protected_document_admin_write():
    """Test that admin can write to documents."""
    doc = ProtectedDocumentProxy("report.txt", "admin")

    result = doc.write("Important data")
    assert "Written to report.txt" in result

    read_result = doc.read()
    assert "Important data" in read_result


def test_protected_document_user_write_denied():
    """Test that regular users cannot write to documents."""
    doc = ProtectedDocumentProxy("report.txt", "user")

    result = doc.write("Some data")
    assert "Access denied" in result
    assert "admin role required" in result


def test_protected_document_role_based_access():
    """Test role-based access control."""
    admin_doc = ProtectedDocumentProxy("file.txt", "admin")
    user_doc = ProtectedDocumentProxy("file.txt", "user")

    admin_result = admin_doc.write("Admin content")
    user_result = user_doc.write("User content")

    assert "Written" in admin_result
    assert "Access denied" in user_result


def test_proxy_internet_blocks_banned_hosts_and_their_subdomains():
    """The ban applies to the host name, however the URL is written."""
    internet = ProxyInternet()

    assert "Access denied" in internet.connect("http://www.banned.com/page")
    assert "Access denied" in internet.connect("https://restricted.net")
    assert "Access denied" in internet.connect("banned.com")


def test_proxy_internet_does_not_block_a_host_that_merely_contains_a_banned_name():
    """unbanned.com is not banned.com."""
    internet = ProxyInternet()

    assert (
        internet.connect("https://unbanned.com") == "Connected to https://unbanned.com"
    )
    assert internet.connect("notbanned.com/banned.com") == (
        "Connected to notbanned.com/banned.com"
    )
