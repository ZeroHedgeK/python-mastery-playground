"""
Magic methods in action: arithmetic, comparisons, container protocols, repr/str,
and callable objects. Includes a "wrong way" example showing why __radd__ and
__iadd__ matter for interoperability.
"""

from __future__ import annotations

import functools

from python_mastery.oop import magic_methods as _library_reference  # noqa: F401


class Money:
    """Simple value object with arithmetic dunders."""

    def __init__(self, amount: int, currency: str = "USD") -> None:
        self.amount = amount
        self.currency = currency

    def __add__(self, other):
        if isinstance(other, Money) and other.currency == self.currency:
            return Money(self.amount + other.amount, self.currency)
        return NotImplemented

    def __radd__(self, other):
        # Supports sum() where start is 0
        if other == 0:
            return self
        return self.__add__(other)

    def __iadd__(self, other):
        if isinstance(other, Money) and other.currency == self.currency:
            self.amount += other.amount
            return self
        return NotImplemented

    def __repr__(self) -> str:
        return f"Money({self.amount}, '{self.currency}')"


@functools.total_ordering
class Priority:
    """Comparable object using __eq__ and __lt__ only."""

    def __init__(self, level: int) -> None:
        self.level = level

    def __eq__(self, other):
        if not isinstance(other, Priority):
            return NotImplemented
        return self.level == other.level

    def __lt__(self, other):
        if not isinstance(other, Priority):
            return NotImplemented
        return self.level < other.level

    def __repr__(self) -> str:
        return f"Priority({self.level})"


class Playlist:
    """Container protocol: len, iteration, indexing, membership."""

    def __init__(self, *tracks: str) -> None:
        self._tracks = list(tracks)

    def __len__(self) -> int:
        return len(self._tracks)

    def __iter__(self):
        return iter(self._tracks)

    def __getitem__(self, index):
        return self._tracks[index]

    def __contains__(self, item: str) -> bool:
        return item in self._tracks

    def __repr__(self) -> str:
        return f"Playlist({self._tracks!r})"

    def __str__(self) -> str:
        return ", ".join(self._tracks)


class Greeter:
    """Callable object behaves like a function but holds state."""

    def __init__(self, greeting: str) -> None:
        self.greeting = greeting

    def __call__(self, name: str) -> str:
        return f"{self.greeting}, {name}!"

    def __repr__(self) -> str:
        return f"Greeter({self.greeting!r})"


def example_arithmetic_dunders() -> None:
    print("\nExample 1: Arithmetic dunders and why __radd__/__iadd__ matter")
    wallet = Money(50)
    tip = Money(10)
    print("  wallet + tip ->", wallet + tip)

    wallet += tip
    print("  wallet after += ->", wallet)

    total = sum([Money(5), Money(15), Money(20)], start=Money(0))
    print("  sum with start Money(0) ->", total)

    print("  wrong way: forgetting __radd__ makes sum([Money(5)]) fail because 0 + Money is unsupported")


def example_comparisons() -> None:
    print("\nExample 2: Comparisons via total_ordering")
    p1, p2, p3 = Priority(1), Priority(2), Priority(2)
    print("  p1 < p2 ->", p1 < p2)
    print("  p2 == p3 ->", p2 == p3)
    print("  sorted priorities ->", sorted([p2, p1, p3]))


def example_container_protocol() -> None:
    print("\nExample 3: Container dunders")
    playlist = Playlist("Intro", "Verse", "Chorus")
    print("  len ->", len(playlist))
    print("  iteration ->", list(playlist))
    print("  index 1 ->", playlist[1])
    print("  'Chorus' in playlist ->", "Chorus" in playlist)
    print("  __repr__ ->", repr(playlist))
    print("  __str__  ->", str(playlist))


def example_callable_objects() -> None:
    print("\nExample 4: __call__ for stateful function objects")
    hello = Greeter("Hello")
    aloha = Greeter("Aloha")
    print("  hello('Ada') ->", hello("Ada"))
    print("  aloha('Linus') ->", aloha("Linus"))


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING MAGIC METHODS")
    print("=" * 70)

    example_arithmetic_dunders()
    example_comparisons()
    example_container_protocol()
    example_callable_objects()

    print("\nAll magic method examples completed.")


if __name__ == "__main__":
    run_all()
