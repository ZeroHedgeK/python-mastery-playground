"""Advanced control-flow patterns: pipelines, pattern matching, and for-else."""

from collections.abc import Iterable, Iterator
from typing import Any, Generator


def process_command(command: Any) -> str:
    """Handle commands using structural pattern matching.

    Demonstrates matching literals, sequences, mappings, and a catch-all case.
    """

    match command:
        case "quit":
            return "Exiting"
        case ["load", filename]:
            return f"Loading {filename}"
        case {"action": "connect", "host": host, "port": port}:
            return f"Connecting to {host}:{port}"
        case ["log", *messages] if messages:
            joined = ", ".join(messages)
            return f"Log entries: {joined}"
        case _:
            return "Unknown command"


def _to_ints(stream: Iterable[Any]) -> Iterator[int]:
    """Convert incoming items to ints, skipping failures (EAFP style)."""

    for item in stream:
        try:
            yield int(item)
        except (TypeError, ValueError):
            continue


def _only_even(stream: Iterable[int]) -> Iterator[int]:
    for value in stream:
        if value % 2 == 0:
            yield value


def _squares(stream: Iterable[int]) -> Iterator[int]:
    for value in stream:
        yield value * value


def pipeline_errors(items: Iterable[Any]) -> list[int]:
    """Run a defensive pipeline: to_ints -> only_even -> squares."""

    return list(_squares(_only_even(_to_ints(items))))


def demonstrate_pipeline() -> list[int]:
    """Demonstrate generator-based processing without materializing intermediates."""

    data = ["4", "not-a-number", 3, 10, "7"]
    return pipeline_errors(data)


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    for divisor in range(2, int(n**0.5) + 1):
        if n % divisor == 0:
            return False
    return True


def find_first_prime(values: Iterable[int]) -> int | None:
    """Return the first prime using for-else; else branch runs when none found."""

    for value in values:
        if _is_prime(value):
            return value
    else:
        return None


def demonstrate_for_else() -> tuple[int | None, int | None]:
    """Show for-else behavior with prime search success and failure cases."""

    found = find_first_prime([4, 6, 9, 11, 15])
    missing = find_first_prime([4, 6, 8, 10])
    return found, missing


def demonstrate_pattern_matching() -> list[str]:
    """Run several pattern-matching scenarios and return their messages."""

    samples: list[Any] = [
        "quit",
        ["load", "data.csv"],
        {"action": "connect", "host": "localhost", "port": 8080},
        ["log", "a", "b"],
        ["noop"],
    ]
    return [process_command(sample) for sample in samples]
