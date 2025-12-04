"""
Type-safety patterns in tests: Protocols, TypedDict, generics, Literals, Final,
Annotated. Demonstrates runtime_checkable Protocols for verifying test doubles
and comments on mypy catching issues before runtime.
"""

from __future__ import annotations

from typing import (
    Annotated,
    Final,
    Generic,
    Literal,
    Protocol,
    TypedDict,
    TypeVar,
    runtime_checkable,
)

import pytest

from python_mastery.testing_patterns import (
    type_safety as _library_reference,
)  # noqa: F401


T = TypeVar("T")
Bounded = TypeVar("Bounded", bound=int)


@runtime_checkable
class Processor(Protocol):
    name: str

    def process(self, data: str) -> int: ...


class UpperProcessor:
    def __init__(self) -> None:
        self.name = "upper"

    def process(self, data: str) -> int:
        return len(data.upper())


class Repo(Generic[T]):
    def __init__(self):
        self.items: list[T] = []

    def add(self, item: T) -> None:
        self.items.append(item)


class UserDict(TypedDict):
    id: int
    name: str
    email: str


def length_if_positive(value: Bounded) -> int:
    return value + 1


Status = Literal["pending", "done"]
MAX_RETRIES: Final[int] = 3
AnnotatedStr = Annotated[str, "metadata:nonempty"]


# === DEMONSTRATIONS ===


def demo_protocol_and_runtime_checkable():
    proc = UpperProcessor()
    print("Processor name ->", proc.name)
    print("isinstance(proc, Processor) ->", isinstance(proc, Processor))

    class BadProcessor:
        pass

    bad = BadProcessor()
    print("isinstance(bad, Processor) ->", isinstance(bad, Processor))
    # mypy would flag: Missing attribute 'process' and 'name'


def demo_generics_and_typed_dict():
    repo = Repo[UserDict]()
    user: UserDict = {"id": 1, "name": "Ada", "email": "ada@example.com"}
    repo.add(user)
    print("Repo items ->", repo.items)


def demo_literal_final_annotated():
    status: Status = "pending"
    print("Status ->", status)
    print("MAX_RETRIES is Final ->", MAX_RETRIES)
    text: AnnotatedStr = "hello"
    print("Annotated text ->", text)


# === PYTEST TESTS ===


def test_protocol_accepts_structural_impl():
    proc = UpperProcessor()
    assert isinstance(proc, Processor)
    assert proc.process("hi") == 2


def test_protocol_rejects_missing_attributes():
    class Incomplete:
        def process(self, data: str) -> int:
            return 0

    obj = Incomplete()
    assert not isinstance(obj, Processor)  # missing name attribute


def test_generics_and_bounds():
    assert length_if_positive(5) == 6
    with pytest.raises(TypeError):
        length_if_positive("not int")  # type: ignore[arg-type]


def test_typed_dict_usage():
    user: UserDict = {"id": 2, "name": "Bob", "email": "bob@example.com"}
    assert user["id"] == 2


def test_literal_and_final():
    status: Status = "done"
    assert status in ("pending", "done")
    assert MAX_RETRIES == 3


# === MAIN ===


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Patterns: Type Safety")
    print("=" * 60)
    demo_protocol_and_runtime_checkable()
    demo_generics_and_typed_dict()
    demo_literal_final_annotated()
    print("\nRun 'pytest examples/test_type_safety.py -v' to execute tests")
