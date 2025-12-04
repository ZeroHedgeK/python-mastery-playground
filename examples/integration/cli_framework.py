"""
CLI framework integration: pattern matching + OOP command pattern + decorators.

Why this combination: pattern matching routes commands declaratively, decorators
register new commands with minimal boilerplate, and OOP encapsulates behaviors.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List

# [PATTERN MATCHING] reference import
from python_mastery.control_flow import advanced_flow as _flow_reference  # noqa: F401

# [DECORATOR] reuse timer for instrumentation
from python_mastery.decorators import timer

# [OOP] reference import for alignment
from python_mastery.oop import advanced_classes as _oop_reference  # noqa: F401


CommandFactory = Callable[[List[str]], "Command"]

registry: Dict[str, CommandFactory] = {}


def command(name: str) -> Callable[[CommandFactory], CommandFactory]:
    """[DECORATOR] Register a command factory by name."""

    def wrapper(factory: CommandFactory) -> CommandFactory:
        registry[name] = factory
        return factory

    return wrapper


@dataclass
class Command:
    args: List[str]

    def run(self) -> str:  # pragma: no cover - demo only
        raise NotImplementedError


@command("greet")
def make_greet(args: List[str]) -> Command:
    class Greet(Command):
        @timer  # [DECORATOR]
        def run(self) -> str:
            name = self.args[0] if self.args else "World"
            return f"Hello, {name}!"

    return Greet(args)


@command("sum")
def make_sum(args: List[str]) -> Command:
    class Summation(Command):
        def run(self) -> str:
            total = sum(int(x) for x in self.args)
            return f"Sum = {total}"

    return Summation(args)


def naive_dispatch(argv: List[str]) -> None:
    """
    Failure-first: if/elif chain is brittle; new commands require edits here.
    """

    print("\n[naive] dispatch using if/elif chain")
    if not argv:
        print("  no command")
        return
    cmd, *args = argv
    if cmd == "greet":
        print(f"  greet -> Hello, {args[0] if args else 'World'}!")
    elif cmd == "sum":
        print(f"  sum -> {sum(int(x) for x in args)}")
    else:
        print("  unknown command; update the chain to add support")


def matched_dispatch(argv: List[str]) -> None:
    """
    Full solution: match/case + registry-driven factories.
    """

    print("\n[matched] dispatch using match/case + registry")
    match argv:  # [PATTERN MATCHING]
        case []:
            print("  no command provided")
            return
        case [cmd, *args]:
            factory = registry.get(cmd)
            if not factory:
                print("  unknown command ->", cmd)
                return
            instance = factory(args)
            print("  result ->", instance.run())


@command("help")
def make_help(args: List[str]) -> Command:
    class Help(Command):
        def run(self) -> str:
            return "Commands: " + ", ".join(sorted(registry))

    return Help(args)


def add_new_command_minimal() -> None:
    """Demonstrate adding a new command without touching dispatch logic."""

    @command("echo")
    def make_echo(args: List[str]) -> Command:
        class Echo(Command):
            def run(self) -> str:
                return " ".join(self.args)

        return Echo(args)

    print("  registered new command 'echo' via decorator only")


def explain_synergy() -> None:
    print("\nWhy this combination matters:")
    print("  • match/case keeps routing explicit and readable")
    print("  • Decorators register commands without editing dispatcher")
    print("  • OOP command classes encapsulate behavior and enable reuse")


def run_demo() -> None:
    naive_dispatch(["unknown"])

    add_new_command_minimal()

    matched_dispatch(["greet", "Ada"])
    matched_dispatch(["sum", "1", "2", "3"])
    matched_dispatch(["help"])
    matched_dispatch(["echo", "hello", "world"])
    explain_synergy()


if __name__ == "__main__":
    run_demo()
