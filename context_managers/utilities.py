"""
Context Manager Utilities
========================

This module demonstrates powerful utilities from the 'contextlib' standard library.
Mastering these prevents you from reinventing the wheel.
"""

import os
from contextlib import suppress, closing, nullcontext, ExitStack
from urllib.request import urlopen

def demonstrate_suppress():
    """
    contextlib.suppress(*exceptions)

    A superior alternative to try/except pass. It explicitly silences
    specified exceptions.
    """
    print("\n--- demonstrate_suppress ---")

    # OLD WAY:
    try:
        os.remove("non_existent_file.tmp")
    except FileNotFoundError:
        pass

    # NEW WAY: Explicit and readable
    with suppress(FileNotFoundError):
        os.remove("non_existent_file.tmp")
    print("Successfully suppressed FileNotFoundError")


def demonstrate_closing():
    """
    contextlib.closing(thing)

    Wraps objects that have a .close() method but don't support the
    context manager protocol natively.
    """
    print("\n--- demonstrate_closing ---")

    # Simulating a class that has close() but no __enter__/__exit__
    class DatabaseConnection:
        def query(self):
            print("Executing query...")
        def close(self):
            print("Connection closed.")

    # with DatabaseConnection() as db:  # This would raise AttributeError

    with closing(DatabaseConnection()) as db:
        db.query()


def demonstrate_nullcontext():
    """
    contextlib.nullcontext(enter_result=None)

    A no-op context manager. Essential for conditional context managers
    to avoid code duplication.
    """
    print("\n--- demonstrate_nullcontext ---")

    use_timeout = False

    # Instead of writing two if/else blocks with duplicated logic:
    # context = Timeout(5) if use_timeout else nullcontext()
    # with context:
    #     ...

    with nullcontext() as ctx:
        print("Running inside a null context (does nothing)")


def demonstrate_exit_stack():
    """
    contextlib.ExitStack()

    The "Swiss Army Knife" of context managers.
    Crucial for:
    1. Managing a dynamic number of context managers (e.g. list of files)
    2. Combining different types of context managers
    """
    print("\n--- demonstrate_exit_stack ---")

    filenames = ["file1.tmp", "file2.tmp", "file3.tmp"]

    # Create dummy files first
    for f in filenames:
        with open(f, "w") as f_obj:
            f_obj.write(f"Content of {f}")

    try:
        # Challenge: How to open ALL files at once?
        # 'with open(f1), open(f2)...' requires knowing the number of files beforehand.

        with ExitStack() as stack:
            # Dynamically enter contexts
            files = [stack.enter_context(open(f)) for f in filenames]

            print(f"Opened {len(files)} files simultaneously:")
            for f in files:
                print(f" - {f.name}: {f.read()}")

            # When this block exits, stack.close() is called, closing ALL files
            # in reverse order.
    finally:
        # Cleanup
        with suppress(FileNotFoundError):
            for f in filenames:
                os.remove(f)


if __name__ == "__main__":
    demonstrate_suppress()
    demonstrate_closing()
    demonstrate_nullcontext()
    demonstrate_exit_stack()

