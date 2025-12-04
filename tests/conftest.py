"""
Shared pytest fixtures for the Python Mastery Playground test suite.

This module provides common fixtures used across multiple test modules,
reducing code duplication and ensuring consistent test setup.
"""

import os
import tempfile
from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# ============================================================================
# Environment Fixtures
# ============================================================================


@pytest.fixture
def clean_env() -> Generator[dict, None, None]:
    """
    Provides a clean environment dictionary and restores original env after test.

    Yields:
        dict: Copy of the original environment for reference.
    """
    original_env = os.environ.copy()
    yield original_env
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def temp_env_var():
    """
    Factory fixture to temporarily set environment variables.

    Returns:
        Callable: Function to set temporary env vars that auto-restore.

    Example:
        def test_something(temp_env_var):
            temp_env_var("API_KEY", "test_value")
            assert os.environ["API_KEY"] == "test_value"
    """
    original_values = {}

    def _set_env(key: str, value: str):
        if key not in original_values:
            original_values[key] = os.environ.get(key)
        os.environ[key] = value

    yield _set_env

    # Restore original values
    for key, original in original_values.items():
        if original is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = original


# ============================================================================
# Timing Fixtures
# ============================================================================


@pytest.fixture
def mock_time():
    """
    Provides a mock time controller for testing time-dependent code.

    Yields:
        MagicMock: Mock object with controllable time.perf_counter().

    Example:
        def test_timer(mock_time):
            mock_time.perf_counter.side_effect = [0.0, 1.5]
            # First call returns 0.0, second returns 1.5
    """
    with patch("time.perf_counter") as mock_perf:
        yield mock_perf


@pytest.fixture
def mock_sleep():
    """
    Mocks time.sleep to avoid actual delays in tests.

    Yields:
        MagicMock: Mock object tracking sleep calls.
    """
    with patch("time.sleep") as mock_slp:
        yield mock_slp


# ============================================================================
# Temporary File Fixtures
# ============================================================================


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """
    Creates a temporary directory that is cleaned up after the test.

    Yields:
        Path: Path to the temporary directory.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_file(temp_dir: Path):
    """
    Factory fixture to create temporary files.

    Args:
        temp_dir: Injected temporary directory fixture.

    Returns:
        Callable: Function to create temp files with content.

    Example:
        def test_file(temp_file):
            path = temp_file("test.txt", "Hello, World!")
            assert path.read_text() == "Hello, World!"
    """

    def _create_file(name: str, content: str = "") -> Path:
        file_path = temp_dir / name
        file_path.write_text(content)
        return file_path

    return _create_file


# ============================================================================
# Mock Service Fixtures
# ============================================================================


@pytest.fixture
def mock_payment_gateway():
    """
    Creates a mock PaymentGateway for testing without real API calls.

    Returns:
        MagicMock: Mock gateway with configurable behavior.

    Example:
        def test_payment(mock_payment_gateway):
            mock_payment_gateway.charge.return_value = True
            result = process_payment(mock_payment_gateway)
            assert result == "success"
    """
    gateway = MagicMock()
    gateway.charge.return_value = True
    return gateway


@pytest.fixture
def mock_repository():
    """
    Creates a mock Repository for testing data access.

    Returns:
        MagicMock: Mock repository with save/get methods.
    """
    repo = MagicMock()
    repo.save.return_value = True
    repo.get.return_value = {"id": 1, "data": "test"}
    return repo


# ============================================================================
# Sample Data Fixtures
# ============================================================================


@pytest.fixture
def sample_user_data() -> dict:
    """
    Provides sample user data for testing.

    Returns:
        dict: User data dictionary.
    """
    return {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "is_active": True,
    }


@pytest.fixture
def sample_numbers() -> list[int]:
    """
    Provides a sample list of numbers for testing.

    Returns:
        list[int]: List of test numbers.
    """
    return [1, 2, 3, 4, 5, 10, 20, 50, 100]


@pytest.fixture
def sample_text() -> str:
    """
    Provides sample text for testing text processing.

    Returns:
        str: Sample text string.
    """
    return "Hello World! This is a test string with Numbers 123 and UPPERCASE."


# ============================================================================
# Function Call Tracking
# ============================================================================


@pytest.fixture
def call_counter():
    """
    Factory fixture that creates call counters for tracking function invocations.

    Returns:
        Callable: Function to create and track call counts.

    Example:
        def test_retries(call_counter):
            counter = call_counter()

            @retry(max_attempts=3)
            def flaky():
                counter()
                if counter.count < 3:
                    raise ValueError("Not yet")
                return "success"

            result = flaky()
            assert counter.count == 3
    """

    def _create_counter():
        class Counter:
            def __init__(self):
                self.count = 0

            def __call__(self):
                self.count += 1
                return self.count

            def reset(self):
                self.count = 0

        return Counter()

    return _create_counter
