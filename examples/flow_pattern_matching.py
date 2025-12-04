"""
Structural pattern matching examples (Python 3.10+). Shows literals, captures,
sequences, mappings, class patterns, OR patterns, guards, and nested cases with
realistic inputs like commands and API responses. Includes comments contrasting
with equivalent if/elif chains.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

from python_mastery.control_flow import (  # noqa: F401
    advanced_flow as _library_reference,
)

if sys.version_info < (3, 10):
    raise SystemExit("Python 3.10+ required for match/case examples")


@dataclass
class Point:
    x: int
    y: int


def example_literals_and_or() -> None:
    print("\nExample 1: Literal and OR patterns for commands")
    for cmd in ["yes", "Y", "no", "maybe"]:
        match cmd:
            case "yes" | "y" | "Y":
                action = "proceed"
            case "no" | "n" | "N":
                action = "abort"
            case _:
                action = "prompt again"
        print(f"  {cmd!r} -> {action}")

    # Equivalent (commented) if/elif would repeat comparisons:
    # if cmd in ("yes", "y", "Y"):
    #     action = "proceed"
    # elif cmd in ("no", "n", "N"):
    #     action = "abort"
    # else:
    #     action = "prompt again"


def example_captures_and_guards() -> None:
    print("\nExample 2: Captures with guard clauses")
    for value in [10, -5, 0]:
        match value:
            case x if x > 0:
                result = f"positive {x}"
            case x if x < 0:
                result = f"negative {x}"
            case _:
                result = "zero"
        print(f"  {value} -> {result}")


def example_sequence_patterns() -> None:
    print("\nExample 3: Sequence patterns with unpacking")
    payloads = [["PING", 123], ["DATA", 1, 2, 3], []]
    for p in payloads:
        match p:
            case ["PING", correlation_id]:
                print(f"  ping with id={correlation_id}")
            case ["DATA", first, *rest]:
                print(f"  data first={first}, rest={rest}")
            case []:
                print("  empty message")
            case _:
                print("  unknown sequence")


def example_mapping_and_nested() -> None:
    print("\nExample 4: Mapping + nested class patterns")
    events = [
        {"type": "move", "point": Point(0, 5)},
        {"type": "move", "point": Point(3, 0)},
        {"type": "click", "button": "left"},
    ]

    for ev in events:
        match ev:
            case {"type": "move", "point": Point(x=0, y=y)}:
                print(f"  vertical move y={y}")
            case {"type": "move", "point": Point(x=x, y=0)}:
                print(f"  horizontal move x={x}")
            case {"type": "click", "button": btn}:
                print(f"  click with {btn}")
            case _:
                print("  fallback event")


def example_real_world_response() -> None:
    print("\nExample 5: API response routing (nested patterns)")
    responses = [
        {"status": 200, "data": {"users": [1, 2, 3]}},
        {"status": 404, "error": "missing"},
        {"status": 500, "error": "crash"},
    ]

    for resp in responses:
        match resp:
            case {"status": 200, "data": {"users": users}}:
                print(f"  success with {len(users)} users")
            case {"status": 404, "error": msg}:
                print(f"  not found: {msg}")
            case {"status": code, "error": msg} if code >= 500:
                print(f"  server error {code}: {msg}")
            case _:
                print("  unrecognized response")

    # If/elif equivalent would nest dict checks and len() calls, harder to read.


def example_when_not_to_use_match() -> None:
    print("\nExample 6: Anti-pattern — simple checks don't need match")
    flag = True
    # Better: just use if flag: ... else: ...
    match flag:
        case True:
            print("  using match here adds noise; prefer simple if")
        case _:
            print("  unreachable")


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING PATTERN MATCHING")
    print("=" * 70)

    example_literals_and_or()
    example_captures_and_guards()
    example_sequence_patterns()
    example_mapping_and_nested()
    example_real_world_response()
    example_when_not_to_use_match()

    print("\nAll pattern matching examples completed.")


if __name__ == "__main__":
    run_all()
