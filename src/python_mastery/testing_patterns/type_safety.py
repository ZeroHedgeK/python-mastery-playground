"""
Type Safety & Static Analysis
============================

Python is dynamically typed, but Type Hints allow for static analysis tools like 'mypy'
to catch bugs before runtime.
"""

from typing import List, Protocol, Sequence, TypedDict, TypeVar

# 1. Generics
# TypeVar allows us to define a variable that represents "any type"
T = TypeVar("T")


def process_items(items: Sequence[T]) -> List[T]:
    """
    A generic function that works with any sequence (list, tuple)
    and returns a list of the same type.
    """
    return list(reversed(items))


# 2. Protocols (Structural Subtyping)
# A Protocol defines what methods an object MUST have.
# Classes don't need to explicitly inherit from it (like interfaces in Go).


class Repository(Protocol):
    def save(self, data: dict) -> bool: ...

    def get(self, id: int) -> dict: ...


class SQLRepository:
    """Satisfies Repository protocol implicitly"""

    def save(self, data: dict) -> bool:
        print("Saving to SQL...")
        return True

    def get(self, id: int) -> dict:
        return {"id": id, "source": "SQL"}


class FileRepository:
    """Also satisfies Repository protocol"""

    def save(self, data: dict) -> bool:
        print("Saving to File...")
        return True

    def get(self, id: int) -> dict:
        return {"id": id, "source": "File"}


def save_user(repo: Repository, user_data: dict):
    """
    This function accepts ANY object that follows the Repository protocol.
    It doesn't care if it's SQL, File, or Mock.
    """
    repo.save(user_data)


# 3. TypedDict
# For when you have a dictionary but want to enforce its structure
class User(TypedDict):
    id: int
    username: str
    email: str
    is_active: bool


def create_user(u: User) -> None:
    print(f"Created user: {u['username']}")


# Usage demonstration
if __name__ == "__main__":
    # Generics
    print(process_items([1, 2, 3]))
    print(process_items(["a", "b", "c"]))

    # Protocols
    sql_repo = SQLRepository()
    save_user(sql_repo, {"name": "Alice"})

    # TypedDict
    alice: User = {
        "id": 1,
        "username": "alice",
        "email": "alice@example.com",
        "is_active": True,
    }
    create_user(alice)
