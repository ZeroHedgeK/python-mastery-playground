"""
Testing & Quality Patterns
=========================

This module covers advanced techniques for ensuring code quality and robustness.
1. Type Safety (Generics, Protocols)
2. Advanced Testing (Fixtures, Mocking, Parametrization)
"""

from .external_services import PaymentGateway, UserManager
from .type_safety import Repository, User, process_items

__all__ = [
    "process_items",
    "Repository",
    "User",
    "PaymentGateway",
    "UserManager",
]
