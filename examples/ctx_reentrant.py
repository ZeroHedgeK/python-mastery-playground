"""
Illustrate single-use vs reusable (reentrant) context managers.

We compare `SingleUse` (raises if reused) with `Reusable` (tracks usage count).
Examples cover normal use, reuse failure, multiple entries, and exception flow
to show `__exit__` still runs.
"""

from __future__ import annotations

from python_mastery.context_managers import Reusable, SingleUse


def example_single_use_once() -> None:
    print("\nExample 1: SingleUse works the first time")
    cm = SingleUse()
    with cm:
        print("  inside SingleUse (first run)")


def example_single_use_reuse_error() -> None:
    print("\nExample 2: SingleUse cannot be re-entered")
    cm = SingleUse()
    with cm:
        print("  initial use succeeds")
    try:
        print("  attempting reuse...")
        with cm:
            print("  should not reach here")
    except RuntimeError as exc:
        print(f"  caught expected reuse error: {exc}")


def example_reusable_multiple_times() -> None:
    print("\nExample 3: Reusable can enter multiple times")
    cm = Reusable()
    for i in range(3):
        with cm:
            print(f"  inside Reusable run #{i + 1}")


def example_exception_handling() -> None:
    print("\nExample 4: __exit__ still runs on exceptions")
    cm = Reusable()
    try:
        with cm:
            print("  inside reusable; about to raise")
            raise ValueError("simulated error during work")
    except ValueError as exc:
        print(f"  caught: {exc}")


def real_world_hint() -> None:
    print("\nExample 5: Where reentrancy matters")
    print(
        "  Reusable patterns mirror locks or pooled connections—enter/exit many times\n"
        "  while enforcing consistent setup/cleanup. SingleUse mirrors one-shot resources\n"
        "  like temporary files that should not be reopened after closing."
    )


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING REENTRANT VS SINGLE-USE CONTEXT MANAGERS")
    print("=" * 70)

    example_single_use_once()
    example_single_use_reuse_error()
    example_reusable_multiple_times()
    example_exception_handling()
    real_world_hint()

    print("\nAll reentrancy examples completed.")


if __name__ == "__main__":
    run_all()
