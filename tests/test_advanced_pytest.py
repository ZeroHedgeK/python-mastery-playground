"""
Advanced Pytest Patterns
=======================

This module demonstrates professional testing techniques:
1. Fixtures: Reusable setup logic
2. Mocking: Isolating code from dependencies
3. Parametrization: Running one test with multiple inputs
"""

from unittest.mock import MagicMock

import pytest

from python_mastery.testing_patterns.external_services import (
    PaymentGateway,
    UserManager,
)
from python_mastery.testing_patterns.type_safety import process_items

# === 1. FIXTURES ===


@pytest.fixture
def mock_gateway():
    """
    Creates a mock PaymentGateway.
    This fixture runs before each test that requests it.
    """
    # MagicMock creates an object that pretends to be anything you want
    return MagicMock(spec=PaymentGateway)


@pytest.fixture
def user_manager(mock_gateway):
    """
    Creates a UserManager with the MOCKED gateway injected.
    Dependency Injection at work!
    """
    return UserManager(mock_gateway)


# === 2. MOCKING ===


def test_upgrade_success(user_manager, mock_gateway):
    """Test that success path works without calling real API."""

    # Arrange: Configure the mock to return True
    mock_gateway.charge.return_value = True

    # Act
    result = user_manager.upgrade_user(123)

    # Assert
    assert result == "User upgraded successfully"
    # Verify the mock was called correctly
    mock_gateway.charge.assert_called_once_with(99.00, "USD")


def test_upgrade_api_error(user_manager, mock_gateway):
    """Test how code handles exceptions from dependencies."""

    # Arrange: Configure mock to raise an exception
    mock_gateway.charge.side_effect = ConnectionError("Boom")

    # Act
    result = user_manager.upgrade_user(123)

    # Assert
    assert result == "Payment failed - try again later"


# === 3. PARAMETRIZATION ===


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ([1, 2, 3], [3, 2, 1]),
        (["a", "b"], ["b", "a"]),
        ([], []),
    ],
)
def test_process_items_parametrized(test_input, expected):
    """
    Runs 3 times with different inputs.
    Eliminates copy-pasting tests.
    """
    assert process_items(test_input) == expected
