"""
Test doubles integration: testing patterns + Protocol-based OOP + context managers.

Why this combination: Protocols guarantee doubles match the contract, context
managers isolate environment and cleanup, and testing patterns show how to
swap real dependencies for fakes without changing calling code.
"""

from __future__ import annotations

import contextlib
import os
import tempfile
from typing import Protocol

# [CONTEXT MANAGER] for env overrides/cleanup
from python_mastery.context_managers import env_var, timer_context

# [OOP] reference import for alignment
from python_mastery.oop import advanced_classes as _oop_reference  # noqa: F401

# [TESTING] reference import
from python_mastery.testing_patterns import (  # noqa: F401
    external_services as _testing_reference,
)


class DataClient(Protocol):  # [PROTOCOL]
    def read(self, key: str) -> str: ...

    def write(self, key: str, value: str) -> None: ...


class FileClient:
    """Real-ish dependency that persists data to temp files."""

    def __init__(self, root: str):
        self.root = root

    def read(self, key: str) -> str:
        path = os.path.join(self.root, key)
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()

    def write(self, key: str, value: str) -> None:
        path = os.path.join(self.root, key)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(value)


class FakeClient:
    """In-memory fake obeying the same Protocol."""

    def __init__(self):
        self.data: dict[str, str] = {}

    def read(self, key: str) -> str:
        return self.data.get(key, "")

    def write(self, key: str, value: str) -> None:
        self.data[key] = value


def write_and_read(client: DataClient, key: str, value: str) -> str:
    """Production function under test; agnostic to real vs fake client."""

    # [CONTEXT MANAGER] timer_context shows duration without altering logic
    with timer_context("write+read"):
        client.write(key, value)
        return client.read(key)


def naive_without_protocol(fake) -> None:
    """
    Failure-first: passing an object lacking required methods raises at runtime
    because no Protocol enforced the contract.
    """

    print("\n[naive] using object without protocol checks")
    try:
        write_and_read(fake, "k", "v")
    except Exception as exc:
        print("  naive call failed:", exc)


@contextlib.contextmanager
def temp_file_client() -> FileClient:
    """[CONTEXT MANAGER] Manage lifecycle of a temporary FileClient."""

    with tempfile.TemporaryDirectory() as tmp:
        yield FileClient(tmp)


def run_with_real_client() -> None:
    print("\n[real] using FileClient with env override")
    with env_var("DATA_ENV", "real"), temp_file_client() as client:
        result = write_and_read(client, "hello.txt", "real-data")
        print("  env DATA_ENV=", os.environ.get("DATA_ENV"))
        print("  read ->", result)


def run_with_fake_client() -> None:
    print("\n[fake] using FakeClient for fast tests")
    fake = FakeClient()
    result = write_and_read(fake, "hello.txt", "fake-data")
    print("  read ->", result)


def explain_synergy() -> None:
    print("\nWhy this combination matters:")
    print("  • Protocol enforces contract for real and fake clients")
    print("  • Context managers isolate env and cleanup temporary resources")
    print("  • Same test harness can swap dependencies without code changes")


def run_demo() -> None:
    class WrongObject:
        pass

    naive_without_protocol(WrongObject())
    run_with_fake_client()
    run_with_real_client()
    explain_synergy()


if __name__ == "__main__":
    run_demo()
