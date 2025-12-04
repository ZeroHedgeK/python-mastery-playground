"""
Mocking and patching patterns: mocks vs fakes, correct patch location, side
effects, and interaction verification. Demonstrates dependency injection to avoid
over-mocking. Runnable as script and as pytest tests.
"""

from __future__ import annotations

from unittest.mock import MagicMock, Mock, call, patch

import pytest

from python_mastery.testing_patterns import external_services as _library_reference  # noqa: F401


# === DEMONSTRATIONS ===


def demo_basic_mock_calls():
    print("Basic Mock with return_value and call assertions")
    m = Mock(return_value=3)
    assert m(1, 2) == 3
    print("  call args ->", m.call_args)
    m.assert_called_with(1, 2)


def demo_side_effects_and_exceptions():
    print("Side effects: sequences and exceptions")
    m = Mock(side_effect=["first", "second", RuntimeError("boom")])
    print("  first ->", m())
    print("  second ->", m())
    try:
        m()
    except RuntimeError as exc:
        print("  raised ->", exc)


def demo_patch_decorator_and_context():
    print("Patching where used (correct location)")

    def fetch_data(client):
        return client.get("/ping")

    with patch("builtins.print") as fake_print:
        fetch_data(Mock(get=Mock(return_value="pong")))
        fake_print.assert_not_called()  # we didn’t call print inside


def demo_magicmock_for_magic_methods():
    print("MagicMock handles magic methods automatically")
    mm = MagicMock()
    mm.__len__.return_value = 10
    print("  len(mm) ->", len(mm))
    mm.__len__.assert_called()


def demo_dependency_injection_over_patching():
    print("Prefer DI over patching for testability")

    class ApiClient:
        def get(self, path: str) -> str:  # pragma: no cover - example only
            raise RuntimeError("real network not allowed in demo")

    def service(client: ApiClient) -> str:
        return client.get("/status")

    fake = Mock(spec=ApiClient)
    fake.get.return_value = "ok"
    assert service(fake) == "ok"
    fake.get.assert_called_with("/status")
    print("  injected fake avoided patching module globals")


# === PYTEST TESTS ===


def test_mock_return_and_calls():
    m = Mock(return_value=10)
    assert m(5) == 10
    m.assert_called_once_with(5)


def test_patch_object_and_spec():
    class Repo:
        def save(self, item):
            return "saved"

    repo = Repo()
    with patch.object(repo, "save", autospec=True, return_value="ok") as patched:
        assert repo.save({}) == "ok"
        patched.assert_called_with({})


def test_side_effect_exception_sequence():
    m = Mock(side_effect=[1, ValueError("fail")])
    assert m() == 1
    with pytest.raises(ValueError):
        m()


def test_patch_context_manager_location():
    with patch("time.sleep", return_value=None) as fake_sleep:
        import time

        time.sleep(0.01)
        fake_sleep.assert_called_once_with(0.01)


def test_fake_over_mock():
    class FakeClock:
        def __init__(self):
            self.now = 0

        def sleep(self, seconds):
            self.now += seconds

    clock = FakeClock()
    clock.sleep(2)
    assert clock.now == 2


# === MAIN ===


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Patterns: Mocking")
    print("=" * 60)
    demo_basic_mock_calls()
    demo_side_effects_and_exceptions()
    demo_patch_decorator_and_context()
    demo_magicmock_for_magic_methods()
    demo_dependency_injection_over_patching()
    print("\nRun 'pytest examples/test_mocking.py -v' to execute tests")
