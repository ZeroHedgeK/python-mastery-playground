"""
Pytest fixture patterns: scope, parametrization, composition, and built-ins. Shows
setup/teardown with yield, async fixtures, factory fixtures, and how scope affects
execution order. Run as script for demonstrations or with pytest for real tests.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from python_mastery.testing_patterns import (
    type_safety as _library_reference,
)  # noqa: F401


# === DEMONSTRATIONS ===


def demo_fixture_scope_prints():
    print("Scope demo: function vs module vs session")

    @pytest.fixture(scope="session")
    def session_marker():
        print("  [session] setup")
        yield "session"
        print("  [session] teardown")

    @pytest.fixture(scope="module")
    def module_marker():
        print("  [module] setup")
        yield "module"
        print("  [module] teardown")

    @pytest.fixture(scope="function")
    def function_marker():
        print("    [function] setup")
        yield "function"
        print("    [function] teardown")

    # Ad-hoc use via pytest's request factory (for demo purposes only)
    for _ in range(2):
        for dep in (session_marker(), module_marker(), function_marker()):
            next(dep)
        # Teardown function scope immediately to illustrate lifecycle
        try:
            next(dep)  # function teardown
        except StopIteration:
            pass


def demo_parametrized_and_factory(tmp_path: Path):
    print("Parametrized fixtures and factory fixtures")

    @pytest.fixture(params=["json", "csv"])
    def format_fixture(request):
        print(f"  setup for format={request.param}")
        yield request.param
        print(f"  teardown for format={request.param}")

    @pytest.fixture
    def writer_factory(tmp_path):
        def factory(fmt: str):
            file = tmp_path / f"data.{fmt}"
            file.write_text(f"payload for {fmt}")
            return file

        return factory

    for fmt in ("json", "csv"):
        file = writer_factory(tmp_path)(fmt)
        print(f"  wrote {file.name}: {file.read_text()}")


def demo_builtin_fixtures(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys):
    print("Using tmp_path, monkeypatch, capsys built-ins")
    file = tmp_path / "sample.txt"
    file.write_text("hello")
    print("  tmp_path wrote:", file.read_text())

    monkeypatch.setenv("DEMO_FLAG", "1")
    print("  env DEMO_FLAG=", Path.exists)

    print("captured print goes to capsys")
    captured = capsys.readouterr()
    print("  capsys captured so far ->", captured.out.strip())


async def demo_async_fixture():
    print("Async fixture pattern")

    @pytest.fixture
    async def async_dep():
        await asyncio.sleep(0.01)
        return "async ready"

    val = await asyncio.sleep(0, result="async ready")
    print("  async dep ->", val)


# === PYTEST FIXTURES FOR TESTS ===


@pytest.fixture(scope="function")
def numbers():
    print("[fixture] numbers setup")
    yield [1, 2, 3]
    print("[fixture] numbers teardown")


@pytest.fixture(params=[2, 3])
def multiplier(request):
    return request.param


@pytest.fixture
def writer(tmp_path):
    def factory(name: str, content: str) -> Path:
        path = tmp_path / name
        path.write_text(content)
        return path

    return factory


# === PYTEST TESTS ===


def test_parametrized_multiplier(numbers, multiplier):
    # Arrange/Act
    result = [n * multiplier for n in numbers]
    # Assert
    assert all(x % multiplier == 0 for x in result)


def test_writer_factory(writer):
    path = writer("file.txt", "data")
    assert path.read_text() == "data"


@pytest.mark.parametrize("value,expected", [("a", "A"), ("b", "B")])
def test_parametrize_marker(value, expected):
    assert value.upper() == expected


@pytest.mark.asyncio
async def test_async_fixture_like_pattern():
    async def do_work():
        await asyncio.sleep(0)
        return 42

    assert await do_work() == 42


# === MAIN ===


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Patterns: Fixtures")
    print("=" * 60)
    demo_fixture_scope_prints()
    demo_parametrized_and_factory(Path.cwd())
    demo_builtin_fixtures(
        Path.cwd(),
        pytest.MonkeyPatch(),
        type(
            "Capsys", (), {"readouterr": lambda self: type("Out", (), {"out": ""})()}
        )(),
    )
    asyncio.run(demo_async_fixture())
    print("\nRun 'pytest examples/test_fixtures.py -v' to execute tests")
