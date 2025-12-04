"""
Loop control patterns: for/else, while/else, break/continue semantics, and
clean exits from nested loops. Shows search/validation idioms and clarifies when
`else` runs (only if loop wasn’t broken).
"""

from __future__ import annotations

from python_mastery.control_flow import (
    advanced_flow as _library_reference,
)  # noqa: F401


def example_for_else_search() -> None:
    print("\nExample 1: for/else search with fallback")
    data = [2, 4, 6, 8]
    target = 5
    for n in data:
        if n == target:
            print("  found target", n)
            break
    else:
        print("  target not found, else runs")
    # if/elif alternative often needs a flag; for/else removes that flag.


def example_validation_all_pass() -> None:
    print("\nExample 2: for/else validation (all items must satisfy predicate)")
    numbers = [3, 6, 9]
    for n in numbers:
        if n % 3 != 0:
            print("  failed on", n)
            break
    else:
        print("  all divisible by 3")


def example_while_else_retry() -> None:
    print("\nExample 3: while/else retry loop")
    attempts = 0
    max_attempts = 3
    success = False

    while attempts < max_attempts:
        attempts += 1
        if attempts == 2:
            success = True
            print("  succeeded on attempt", attempts)
            break
        print("  attempt", attempts, "failed")
    else:
        print("  exhausted retries without success")

    print("  success=", success)


def example_nested_break_simulation() -> None:
    print("\nExample 4: Breaking out of nested loops cleanly")
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    found = None
    for row in matrix:
        for value in row:
            if value == 5:
                found = value
                break  # breaks inner only
        if found is not None:
            break  # manual outer break (simulate labeled break)
    print("  found:", found)


def example_continue_vs_break() -> None:
    print("\nExample 5: continue vs break vs return semantics")
    for n in range(5):
        if n == 1:
            print("  continue at", n)
            continue
        if n == 3:
            print("  break at", n)
            break
        print("  processing", n)
    else:
        print("  loop finished without break (else would run only then)")


def example_misunderstanding_else() -> None:
    print("\nExample 6: Clarifying loop else")
    # Else runs when loop is not broken, even if body never executes
    for _ in []:
        pass
    else:
        print("  for-else ran even with empty iterable")


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING LOOP CONTROL PATTERNS")
    print("=" * 70)

    example_for_else_search()
    example_validation_all_pass()
    example_while_else_retry()
    example_nested_break_simulation()
    example_continue_vs_break()
    example_misunderstanding_else()

    print("\nAll loop control examples completed.")


if __name__ == "__main__":
    run_all()
