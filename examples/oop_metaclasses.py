"""
Metaclass patterns: class creation hooks, registries, validation, and automatic
augmentation. Shows when metaclasses are justified and when simpler tools
(__init_subclass__, decorators) would suffice.
"""

from __future__ import annotations

from python_mastery.oop import metaclasses as _library_reference  # noqa: F401


def example_basic_metaclass() -> None:
    print("\nExample 1: Basic metaclass injecting defaults")

    class DefaultFields(type):
        def __new__(mcs, name, bases, attrs):
            attrs.setdefault("version", 1)
            cls = super().__new__(mcs, name, bases, attrs)
            return cls

    class Document(metaclass=DefaultFields):
        title = "Untitled"

    doc = Document()
    print("  Document.version ->", doc.version)
    print("  Document.title ->", doc.title)


def example_registry_metaclass() -> None:
    print("\nExample 2: Registry metaclass for plugins")
    registry: list[type] = []

    class PluginMeta(type):
        def __init__(cls, name, bases, attrs):
            super().__init__(name, bases, attrs)
            if bases != (object,):  # skip base class itself
                registry.append(cls)

    class Plugin(metaclass=PluginMeta):
        pass

    class PdfExporter(Plugin):
        format = "pdf"

    class HtmlExporter(Plugin):
        format = "html"

    print("  registered:", [cls.__name__ for cls in registry])


def example_validation_metaclass() -> None:
    print("\nExample 3: Validation at class definition time")

    class RequiresSave(type):
        def __new__(mcs, name, bases, attrs):
            if "save" not in attrs:
                raise TypeError("Classes must define a save() method")
            return super().__new__(mcs, name, bases, attrs)

    class Model(metaclass=RequiresSave):
        def save(self):
            print("saving...")

    try:

        class BrokenModel(metaclass=RequiresSave):
            pass

    except TypeError as exc:
        print("  validation caught:", exc)

    Model().save()


def example_auto_methods() -> None:
    print("\nExample 4: Auto-adding methods via metaclass")

    class AutoStr(type):
        def __new__(mcs, name, bases, attrs):
            if "__str__" not in attrs:

                def __str__(self):  # type: ignore[no-untyped-def]
                    return f"<auto {name} {self.__dict__}>"

                attrs["__str__"] = __str__
            return super().__new__(mcs, name, bases, attrs)

    class Record(metaclass=AutoStr):
        def __init__(self, **fields):
            self.__dict__.update(fields)

    print("  auto-str:", str(Record(id=1, status="ok")))


def example_when_not_to_use_metaclass() -> None:
    print("\nExample 5: Prefer __init_subclass__ or decorators for simpler cases")

    class Decorated:
        labels: list[str] = []

    def add_label(cls):
        cls.labels.append(cls.__name__)
        return cls

    @add_label
    class Simple:
        pass

    print("  Decorator alternative labels:", Decorated.labels)
    print(
        "  Metaclasses are heavier; use them when you truly need class-creation control."
    )


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING METACLASSES")
    print("=" * 70)

    example_basic_metaclass()
    example_registry_metaclass()
    example_validation_metaclass()
    example_auto_methods()
    example_when_not_to_use_metaclass()

    print("\nAll metaclass examples completed.")


if __name__ == "__main__":
    run_all()
