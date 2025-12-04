"""
Python Mastery Playground - Unified CLI
======================================

This is the main entry point for the playground.
It provides an interactive menu to run demonstrations from all modules.
"""

import importlib

MODULES = {
    "1": {
        "title": "Advanced Patterns (Decorators & Context Managers)",
        "demos": [
            (
                "Context Manager Utilities",
                "python_mastery.context_managers.utilities",
                [
                    "demonstrate_suppress",
                    "demonstrate_closing",
                    "demonstrate_nullcontext",
                    "demonstrate_exit_stack",
                ],
            ),
            (
                "Async Context Managers",
                "python_mastery.context_managers.async_ctx",
                ["main"],
            ),
            (
                "State Management",
                "python_mastery.context_managers.state",
                ["demonstrate_state_change"],
            ),
            (
                "Reentrancy",
                "python_mastery.context_managers.reentrant",
                ["demonstrate_reentrancy"],
            ),
        ],
    },
    "2": {
        "title": "Data Structures",
        "demos": [
            (
                "Advanced Built-ins",
                "python_mastery.datastructures.builtins",
                [
                    "demonstrate_slicing",
                    "demonstrate_comprehensions",
                    "demonstrate_generators",
                ],
            ),
            (
                "Collections",
                "python_mastery.datastructures.collections_demo",
                [
                    "demonstrate_counter",
                    "demonstrate_defaultdict",
                    "demonstrate_deque",
                    "demonstrate_namedtuple",
                    "demonstrate_chainmap",
                ],
            ),
        ],
    },
    "3": {
        "title": "Object-Oriented Programming",
        "demos": [
            (
                "Advanced Classes",
                "python_mastery.oop.advanced_classes",
                [
                    "demonstrate_singleton",
                    "demonstrate_slots",
                    "demonstrate_properties",
                ],
            ),
            (
                "Inheritance & MRO",
                "python_mastery.oop.inheritance",
                ["demonstrate_mro", "demonstrate_mixins"],
            ),
            (
                "Magic Methods",
                "python_mastery.oop.magic_methods",
                ["demonstrate_magic_methods"],
            ),
            (
                "Metaclasses",
                "python_mastery.oop.metaclasses",
                ["demonstrate_metaclass"],
            ),
        ],
    },
    "4": {
        "title": "Concurrency",
        "demos": [
            (
                "Threading (I/O)",
                "python_mastery.concurrency.threading_demo",
                ["demonstrate_threading"],
            ),
            (
                "Multiprocessing (CPU)",
                "python_mastery.concurrency.multiprocessing_demo",
                ["demonstrate_multiprocessing"],
            ),
            (
                "AsyncIO",
                "python_mastery.concurrency.asyncio_demo",
                ["demonstrate_asyncio"],
            ),
        ],
    },
    "5": {
        "title": "Testing & Quality",
        "demos": [
            ("Type Safety", "python_mastery.testing_patterns.type_safety", None),
        ],
    },
    "6": {
        "title": "Functional Programming",
        "demos": [
            (
                "Functional Tools",
                "python_mastery.functional.functional_tools",
                ["demonstrate_partial", "demonstrate_reduce", "demonstrate_itertools"],
            ),
            (
                "Immutability",
                "python_mastery.functional.immutability",
                ["demonstrate_frozen_dataclass", "demonstrate_purity"],
            ),
        ],
    },
    "7": {
        "title": "Python Internals",
        "demos": [
            (
                "Bytecode Inspector",
                "python_mastery.internals.bytecode_inspector",
                ["inspect_function"],
            ),
            (
                "Memory Management",
                "python_mastery.internals.memory_management",
                ["demonstrate_ref_counting", "demonstrate_garbage_collection"],
            ),
        ],
    },
}


def run_demo(module_path: str, functions: list[str] | None):
    """Imports a module and runs specific functions or the whole module."""
    try:
        print(f"\n--- Loading {module_path} ---\n")
        mod = importlib.import_module(module_path)

        if functions:
            for func_name in functions:
                if hasattr(mod, func_name):
                    print(f">>> Running {func_name}...")
                    func = getattr(mod, func_name)
                    # Handle async functions if necessary, but our demos wrap them (e.g. demonstrate_asyncio)
                    if callable(func):
                        func()
                    else:
                        print(f"Skipping {func_name} (not callable)")
                    print("-" * 20)
                else:
                    print(f"Warning: Function {func_name} not found in {module_path}")
        else:
            print(f"Module {module_path} imported successfully.")

    except ImportError as e:
        print(f"Error importing {module_path}: {e}")
    except Exception as e:
        print(f"Error running demo: {e}")


def show_menu():
    print("\n" + "=" * 50)
    print("PYTHON MASTERY PLAYGROUND")
    print("=" * 50)

    for key in sorted(MODULES.keys()):
        print(f"{key}. {MODULES[key]['title']}")

    print("q. Quit")
    print("=" * 50)


def main():
    while True:
        show_menu()
        choice = input("Select a module (1-7, q): ").strip().lower()

        if choice == "q":
            print("Goodbye!")
            break

        if choice in MODULES:
            module_info = MODULES[choice]
            print(f"\n=== {module_info['title']} ===")

            for i, (name, _path, _funcs) in enumerate(module_info["demos"], 1):
                print(f"{i}. {name}")

            print("b. Back to Main Menu")

            sub_choice = input("Select a demo: ").strip().lower()

            if sub_choice == "b":
                continue

            try:
                idx = int(sub_choice) - 1
                if 0 <= idx < len(module_info["demos"]):
                    name, path, funcs = module_info["demos"][idx]
                    run_demo(path, funcs)
                    input("\nPress Enter to continue...")
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid selection.")
        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()
