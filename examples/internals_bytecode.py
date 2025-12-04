"""
Bytecode inspection with `dis`: see how Python executes your code. Useful for
understanding costs (LOAD_FAST vs LOAD_GLOBAL, INPLACE vs BINARY ops) and why
certain patterns run faster. CPython-specific: other interpreters may differ.
"""

from __future__ import annotations

import dis
import sys

from python_mastery.internals import bytecode_inspector as _library_reference  # noqa: F401


def simple_add(x: int, y: int) -> int:
    return x + y


def inplace_add(x: int) -> int:
    x += 1
    return x


def loop_sum(items: list[int]) -> int:
    total = 0
    for n in items:
        total += n
    return total


def list_comp(items: list[int]) -> int:
    return sum([n for n in items])


def map_sum(items: list[int]) -> int:
    return sum(map(int, items))


def inspect_function(fn, *args):
    print(f"\n-- disassembly for {fn.__name__} --")
    dis.dis(fn)
    print("  co_consts:", fn.__code__.co_consts)
    print("  co_varnames:", fn.__code__.co_varnames)
    print("  co_stacksize:", fn.__code__.co_stacksize)
    if args:
        print("  sample call result:", fn(*args))


def example_basic_dis() -> None:
    print("\nExample 1: Basic disassembly and __code__ details")
    inspect_function(simple_add, 2, 3)
    # Note LOAD_FAST for locals, BINARY_ADD, RETURN_VALUE


def example_inplace_vs_binary() -> None:
    print("\nExample 2: x = x + 1 vs x += 1")

    def add_then_assign(x: int) -> int:
        x = x + 1
        return x

    print("  add_then_assign bytecode (BINARY_ADD):")
    dis.dis(add_then_assign)
    print("  inplace_add bytecode (INPLACE_ADD):")
    dis.dis(inplace_add)
    print("  INPLACE_ADD may reuse objects (e.g., lists) but ints are immutable so CPython makes a new int anyway.")


def example_loop_vs_comp_vs_map() -> None:
    print("\nExample 3: for-loop vs list comp vs map")
    items = [1, 2, 3]
    inspect_function(loop_sum, items)
    inspect_function(list_comp, items)
    inspect_function(map_sum, items)
    print("  Comprehensions inline BUILD_LIST+LIST_APPEND; map uses CALL_FUNCTION and iterator consumption.")


def example_constant_folding() -> None:
    print("\nExample 4: Constant folding")
    folded = lambda: 2 + 3  # noqa: E731
    dis.dis(folded)
    print("  Note LOAD_CONST 5: compile-time folded.")


def example_compile_and_bytecode_obj() -> None:
    print("\nExample 5: compile() and dis.Bytecode for programmatic inspection")
    src = "total = 0\nfor i in range(3):\n    total += i\n"
    code_obj = compile(src, filename="<string>", mode="exec")
    bytecode = dis.Bytecode(code_obj)
    for instr in bytecode:
        print(f"  {instr.opname:<20} arg={instr.argrepr}")


def example_local_vs_global() -> None:
    print("\nExample 6: LOAD_FAST vs LOAD_GLOBAL")
    g_val = 5

    def uses_local():
        x = 1
        return x + 1

    def uses_global():
        return g_val + 1

    print("  uses_local:")
    dis.dis(uses_local)
    print("  uses_global:")
    dis.dis(uses_global)
    print("  LOAD_FAST is cheaper than LOAD_GLOBAL; prefer locals in hot paths.")


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING BYTECODE INSPECTION")
    print("=" * 70)

    example_basic_dis()
    example_inplace_vs_binary()
    example_loop_vs_comp_vs_map()
    example_constant_folding()
    example_compile_and_bytecode_obj()
    example_local_vs_global()

    print("\nAll bytecode examples completed.")


if __name__ == "__main__":
    run_all()
