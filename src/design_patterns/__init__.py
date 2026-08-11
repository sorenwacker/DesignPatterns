# src/design_patterns/__init__.py

"""
This package demonstrates various software design patterns implemented in Python.
It provides practical examples and explanations of common design patterns to help
developers understand and apply these patterns in their own projects.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ("__version__",)
