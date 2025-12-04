"""
Plugin system integration: metaclasses + decorators + functional partials.

Why this combination: metaclasses auto-register plugins, decorators annotate
intent and wrap behavior, and partials preconfigure plugin instances without
changing core code.
"""

from __future__ import annotations

from functools import partial
from typing import Callable, Dict, List

# [METACLASS] import aligns with library primitives
from python_mastery.oop import metaclasses as _metaclasses_reference  # noqa: F401

# [DECORATOR] reuse a timing decorator for visibility
from python_mastery.decorators import timer

# [FUNCTIONAL] highlight partial/composition
from python_mastery.functional import (
    functional_tools as _functional_reference,
)  # noqa: F401


class PluginMeta(type):
    """Metaclass that auto-registers plugins when subclasses are defined."""

    registry: Dict[str, type] = {}

    def __init__(cls, name, bases, attrs):  # [METACLASS]
        super().__init__(name, bases, attrs)
        if not attrs.get("name"):
            return
        PluginMeta.registry[cls.name] = cls


def plugin(fn: Callable) -> Callable:
    """
    [DECORATOR] Tag a plugin factory to print registration info.
    """

    def wrapper(*args, **kwargs):
        print(f"  registering plugin via decorator: {fn.__name__}")
        return fn(*args, **kwargs)

    return wrapper


class BasePlugin(metaclass=PluginMeta):
    name: str

    def run(self, payload: dict) -> dict:  # pragma: no cover - demo only
        raise NotImplementedError


@plugin
def register_transformer(multiplier: int) -> type[BasePlugin]:
    """Factory returning a configured plugin class using partial-like pattern."""

    class Transformer(BasePlugin):
        name = f"transformer_{multiplier}"

        @timer  # [DECORATOR]
        def run(self, payload: dict) -> dict:
            data = payload.get("value", 0) * multiplier
            return {**payload, "value": data, "stage": self.name}

    return Transformer


@plugin
def register_validator(threshold: int) -> type[BasePlugin]:
    class Validator(BasePlugin):
        name = f"validator_{threshold}"

        def run(self, payload: dict) -> dict:
            if payload.get("value", 0) < threshold:
                raise ValueError("value too small")
            return {**payload, "validated": True, "stage": self.name}

    return Validator


def manual_pipeline(payload: dict) -> None:
    """
    Failure-first path: manual registry and no configuration helpers.
    Adding a new plugin would require editing this function every time.
    """

    print("\n[manual] running without metaclass registry (expect KeyError)")
    registry: Dict[str, type] = {}
    try:
        registry["missing"](payload)  # type: ignore[index]
    except Exception as exc:
        print("  manual pipeline failed:", exc)


def composed_pipeline(payload: dict) -> None:
    """Full solution: metaclass registry + decorator + partial configuration."""

    print("\n[composed] building pipeline via registry + partial")

    # [FUNCTIONAL] partial preconfigures plugin constructors
    transformer_cls = register_transformer(multiplier=3)
    validator_cls = register_validator(threshold=5)

    # Additional plugin with partial to bind environment
    class Annotator(BasePlugin):
        name = "annotator"

        def __init__(self, *, env: str) -> None:
            self.env = env

        def run(self, payload: dict) -> dict:
            return {**payload, "env": self.env, "stage": self.name}

    PluginMeta.registry[Annotator.name] = Annotator  # [METACLASS] manual hook allowed

    pipeline: List[Callable[[dict], dict]] = [
        partial(transformer_cls().run),  # [FUNCTIONAL]
        partial(validator_cls().run),
        partial(Annotator(env="staging").run),
    ]

    state = payload
    for step in pipeline:
        state = step(state)
        print("  step ->", state)

    print("  registry keys:", list(PluginMeta.registry))


def explain_synergy() -> None:
    print("\nWhy this combination matters:")
    print("  • Metaclass registry removes manual plugin bookkeeping")
    print("  • Decorators annotate and instrument plugin creation")
    print("  • partial enables configuration without touching core pipeline")
    print("  • Adding a new plugin only requires defining a subclass")


def run_demo() -> None:
    payload = {"value": 2, "source": "unit-test"}
    manual_pipeline(payload)

    # Increase payload to satisfy validator
    composed_pipeline({**payload, "value": 4})
    composed_pipeline({**payload, "value": 10})
    explain_synergy()


if __name__ == "__main__":
    run_demo()
