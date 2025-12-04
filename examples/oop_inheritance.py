"""
Inheritance patterns: MRO, diamonds, mixins, and cooperative multiple inheritance.

We print `__mro__`, show how `super()` keeps diamond graphs sane, and contrast a
"wrong way" manual base-call that double-invokes parents. Mixins demonstrate
composing focused behaviors.
"""

from __future__ import annotations

from python_mastery.oop import inheritance as _library_reference  # noqa: F401


def example_mro_and_diamond() -> None:
    print("\nExample 1: Diamond inheritance and MRO")

    class Vehicle:
        def start(self) -> None:
            print("Vehicle.start")

    class EngineMixin(Vehicle):
        def start(self) -> None:
            print("EngineMixin.start")
            super().start()

    class BatteryMixin(Vehicle):
        def start(self) -> None:
            print("BatteryMixin.start")
            super().start()

    class HybridCar(EngineMixin, BatteryMixin):
        def start(self) -> None:
            print("HybridCar.start")
            super().start()

    print("  MRO:", [cls.__name__ for cls in HybridCar.__mro__])
    HybridCar().start()


def example_wrong_way_manual_calls() -> None:
    print("\nExample 2: Wrong way — manual base calls cause double work")

    class Base:
        def do_work(self) -> None:
            print("Base.do_work")

    class Left(Base):
        def do_work(self) -> None:
            print("Left.do_work")
            Base.do_work(self)  # ❌ breaks cooperative order

    class Right(Base):
        def do_work(self) -> None:
            print("Right.do_work")
            Base.do_work(self)

    class Diamond(Left, Right):
        def do_work(self) -> None:
            print("Diamond.do_work")
            Left.do_work(self)
            Right.do_work(self)

    print("  MRO:", [cls.__name__ for cls in Diamond.__mro__])
    print("  Calling do_work triggers Base twice (anti-pattern):")
    Diamond().do_work()


def example_mixins() -> None:
    print("\nExample 3: Mixins add focused behavior")

    class JsonMixin:
        def to_json(self) -> str:
            import json

            return json.dumps(self.__dict__)

    class AuditableMixin:
        def audit_label(self) -> str:
            return f"{self.__class__.__name__}:{id(self)}"

    class Order(JsonMixin, AuditableMixin):
        def __init__(self, order_id: int, total: float) -> None:
            self.order_id = order_id
            self.total = total

    order = Order(101, 59.99)
    print("  json:", order.to_json())
    print("  audit:", order.audit_label())


def example_cooperative_super() -> None:
    print("\nExample 4: Cooperative multiple inheritance with super()")

    class Notifier:
        def notify(self, message: str) -> None:
            print("Notifier: base message", message)

    class EmailMixin(Notifier):
        def notify(self, message: str) -> None:
            print("  Email sent")
            super().notify(message)

    class SmsMixin(Notifier):
        def notify(self, message: str) -> None:
            print("  SMS sent")
            super().notify(message)

    class AlertService(EmailMixin, SmsMixin):
        def notify(self, message: str) -> None:
            print("AlertService dispatch")
            super().notify(message)

    service = AlertService()
    print("  MRO:", [cls.__name__ for cls in AlertService.__mro__])
    service.notify("Threshold exceeded")


def example_mro_dispatch_difference() -> None:
    print("\nExample 5: MRO affects which mixin wins")

    class TimestampMixin:
        def label(self) -> str:
            return "timestamp"

    class UserMixin:
        def label(self) -> str:
            return "user"

    class FirstWins(TimestampMixin, UserMixin):
        pass

    class SecondWins(UserMixin, TimestampMixin):
        pass

    print("  FirstWins label:", FirstWins().label())
    print("  SecondWins label:", SecondWins().label())


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING INHERITANCE & MRO")
    print("=" * 70)

    example_mro_and_diamond()
    example_wrong_way_manual_calls()
    example_mixins()
    example_cooperative_super()
    example_mro_dispatch_difference()

    print("\nAll inheritance examples completed.")


if __name__ == "__main__":
    run_all()
