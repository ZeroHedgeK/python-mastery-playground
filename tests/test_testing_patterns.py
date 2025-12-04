"""
test_testing_patterns.py - Unit tests for the testing_patterns module.

Tests cover:
- Type safety patterns (Generics, Protocols, TypedDict)
- External services mocking (PaymentGateway, UserManager)
"""

from unittest.mock import MagicMock, patch

import pytest

from python_mastery.testing_patterns.external_services import (
    PaymentGateway,
    UserManager,
)
from python_mastery.testing_patterns.type_safety import (
    FileRepository,
    SQLRepository,
    User,
    create_user,
    process_items,
    save_user,
)


class TestProcessItems:
    """Tests for the generic process_items function."""

    def test_process_items_with_integers(self):
        """process_items should reverse a list of integers."""
        result = process_items([1, 2, 3, 4, 5])
        assert result == [5, 4, 3, 2, 1]

    def test_process_items_with_strings(self):
        """process_items should reverse a list of strings."""
        result = process_items(["a", "b", "c"])
        assert result == ["c", "b", "a"]

    def test_process_items_with_tuple(self):
        """process_items should work with tuples and return a list."""
        result = process_items((10, 20, 30))
        assert result == [30, 20, 10]
        assert isinstance(result, list)

    def test_process_items_empty_sequence(self):
        """process_items should handle empty sequences."""
        result = process_items([])
        assert result == []

    def test_process_items_single_element(self):
        """process_items should handle single-element sequences."""
        result = process_items([42])
        assert result == [42]

    def test_process_items_mixed_types(self):
        """process_items should work with mixed types."""
        result = process_items([1, "two", 3.0])
        assert result == [3.0, "two", 1]


class TestRepositoryProtocol:
    """Tests for Repository protocol implementations."""

    def test_sql_repository_save(self, capsys):
        """SQLRepository.save should return True and print."""
        repo = SQLRepository()
        result = repo.save({"name": "test"})

        assert result is True
        output = capsys.readouterr().out
        assert "SQL" in output

    def test_sql_repository_get(self):
        """SQLRepository.get should return dict with id and source."""
        repo = SQLRepository()
        result = repo.get(42)

        assert result == {"id": 42, "source": "SQL"}

    def test_file_repository_save(self, capsys):
        """FileRepository.save should return True and print."""
        repo = FileRepository()
        result = repo.save({"name": "test"})

        assert result is True
        output = capsys.readouterr().out
        assert "File" in output

    def test_file_repository_get(self):
        """FileRepository.get should return dict with id and source."""
        repo = FileRepository()
        result = repo.get(99)

        assert result == {"id": 99, "source": "File"}

    def test_save_user_with_sql_repo(self, capsys):
        """save_user should work with SQLRepository."""
        repo = SQLRepository()
        save_user(repo, {"name": "Alice"})

        output = capsys.readouterr().out
        assert "SQL" in output

    def test_save_user_with_file_repo(self, capsys):
        """save_user should work with FileRepository."""
        repo = FileRepository()
        save_user(repo, {"name": "Bob"})

        output = capsys.readouterr().out
        assert "File" in output

    def test_save_user_with_mock_repo(self):
        """save_user should work with any object following Protocol."""
        mock_repo = MagicMock()
        mock_repo.save.return_value = True

        save_user(mock_repo, {"name": "Charlie"})

        mock_repo.save.assert_called_once_with({"name": "Charlie"})


class TestCreateUser:
    """Tests for the create_user function with TypedDict."""

    def test_create_user_valid_data(self, capsys, sample_user_data):
        """create_user should accept valid User TypedDict."""
        user: User = sample_user_data
        create_user(user)

        output = capsys.readouterr().out
        assert "testuser" in output

    def test_create_user_prints_username(self, capsys):
        """create_user should print the username."""
        user: User = {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com",
            "is_active": True,
        }
        create_user(user)

        output = capsys.readouterr().out
        assert "john_doe" in output


class TestPaymentGateway:
    """Tests for the PaymentGateway class (with mocking)."""

    def test_charge_with_mock_sleep(self, mock_sleep):
        """PaymentGateway.charge should work (with mocked sleep)."""
        gateway = PaymentGateway()

        # Patch random to avoid ConnectionError
        with patch("random.random", return_value=0.5):
            result = gateway.charge(99.99, "USD")

        assert result is True
        mock_sleep.assert_called_once_with(2)

    def test_charge_connection_error(self, mock_sleep):
        """PaymentGateway.charge should raise ConnectionError sometimes."""
        gateway = PaymentGateway()

        # Force the random check to trigger an error
        with patch("random.random", return_value=0.05):
            with pytest.raises(ConnectionError, match="Bank API unavailable"):
                gateway.charge(50.00, "EUR")

    def test_charge_prints_message(self, mock_sleep, capsys):
        """PaymentGateway.charge should print connection message."""
        gateway = PaymentGateway()

        with patch("random.random", return_value=0.5):
            gateway.charge(100.00, "GBP")

        output = capsys.readouterr().out
        assert "100" in output or "100.0" in output
        assert "GBP" in output


class TestUserManager:
    """Tests for UserManager with mocked PaymentGateway."""

    def test_upgrade_user_success(self, mock_payment_gateway):
        """UserManager.upgrade_user should return success message."""
        mock_payment_gateway.charge.return_value = True
        manager = UserManager(mock_payment_gateway)

        result = manager.upgrade_user(user_id=1)

        assert result == "User upgraded successfully"
        mock_payment_gateway.charge.assert_called_once_with(99.00, "USD")

    def test_upgrade_user_payment_declined(self, mock_payment_gateway):
        """UserManager.upgrade_user should handle declined payment."""
        mock_payment_gateway.charge.return_value = False
        manager = UserManager(mock_payment_gateway)

        result = manager.upgrade_user(user_id=2)

        assert result == "Payment declined"

    def test_upgrade_user_connection_error(self, mock_payment_gateway):
        """UserManager.upgrade_user should handle connection errors."""
        mock_payment_gateway.charge.side_effect = ConnectionError("Network down")
        manager = UserManager(mock_payment_gateway)

        result = manager.upgrade_user(user_id=3)

        assert result == "Payment failed - try again later"

    def test_upgrade_user_calls_gateway_with_correct_amount(self, mock_payment_gateway):
        """UserManager should charge exactly $99.00 USD."""
        mock_payment_gateway.charge.return_value = True
        manager = UserManager(mock_payment_gateway)

        manager.upgrade_user(user_id=42)

        mock_payment_gateway.charge.assert_called_with(99.00, "USD")


class TestMockingPatterns:
    """Tests demonstrating common mocking patterns."""

    def test_mock_return_value(self):
        """Demonstrate setting mock return values."""
        mock_func = MagicMock()
        mock_func.return_value = "mocked result"

        assert mock_func() == "mocked result"
        assert mock_func("any", "args") == "mocked result"

    def test_mock_side_effect_exception(self):
        """Demonstrate mocking exceptions."""
        mock_func = MagicMock()
        mock_func.side_effect = ValueError("mocked error")

        with pytest.raises(ValueError, match="mocked error"):
            mock_func()

    def test_mock_side_effect_sequence(self):
        """Demonstrate mocking sequences of returns."""
        mock_func = MagicMock()
        mock_func.side_effect = [1, 2, 3]

        assert mock_func() == 1
        assert mock_func() == 2
        assert mock_func() == 3

    def test_mock_call_assertions(self):
        """Demonstrate mock call assertions."""
        mock_func = MagicMock()

        mock_func("arg1", key="value")
        mock_func("arg2")

        assert mock_func.call_count == 2
        mock_func.assert_any_call("arg1", key="value")
        mock_func.assert_called_with("arg2")  # Last call

    def test_patch_module_function(self):
        """Demonstrate patching a module function."""
        with patch(
            "python_mastery.testing_patterns.external_services.time.sleep"
        ) as mock_sleep:
            with patch(
                "python_mastery.testing_patterns.external_services.random.random",
                return_value=0.5,
            ):
                gateway = PaymentGateway()
                gateway.charge(50.00, "USD")

            mock_sleep.assert_called_once_with(2)


class TestIntegrationWithFixtures:
    """Tests using conftest.py fixtures."""

    def test_with_sample_user_data(self, sample_user_data):
        """Test using the sample_user_data fixture."""
        assert sample_user_data["username"] == "testuser"
        assert sample_user_data["is_active"] is True

    def test_with_call_counter(self, call_counter):
        """Test using the call_counter fixture."""
        counter = call_counter()

        counter()
        counter()
        counter()

        assert counter.count == 3

        counter.reset()
        assert counter.count == 0

    def test_repository_with_mock_repo_fixture(self, mock_repository):
        """Test using the mock_repository fixture."""
        result = mock_repository.get(1)
        assert result == {"id": 1, "data": "test"}

        mock_repository.save({"new": "data"})
        mock_repository.save.assert_called_with({"new": "data"})
