"""
Bytecode Inspector
=================

Python code is compiled to 'bytecode' which the CPython interpreter executes.
The 'dis' module allows us to peek at these low-level instructions.
"""

import dis


def example_function(x: int, y: int) -> int:
    """Simple function to demonstrate bytecode inspection."""
    a = x + y
    return a * 2


def inspect_function() -> None:
    """Disassemble a simple function to show its bytecode."""
    print("\n=== Bytecode Inspection ===")
    print(f"Inspecting function: {example_function.__name__}")

    # 'dis.dis' prints the disassembly to stdout
    dis.dis(example_function)

    print("\nExplanation:")
    print("LOAD_FAST: Loads a local variable onto the stack")
    print("BINARY_OP: Performs operation (ADD, MUL)")
    print("RETURN_VALUE: Returns the top stack item")


if __name__ == "__main__":
    inspect_function()
