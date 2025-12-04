"""
Demonstrate temporary state changes with context managers (env vars as example).

We show how `env_var` sets a value, restores on exit, handles nesting, and still
cleans up when exceptions occur. Prints show state before/during/after each
`with` so you can trace the transitions.
"""

from __future__ import annotations

import os

from python_mastery.context_managers import env_var


def example_basic_state_flip() -> None:
    print("\nExample 1: Basic temporary override")
    print(f"  before: API_KEY={os.environ.get('API_KEY')}")
    with env_var("API_KEY", "temp-key-123"):
        print(f"  inside: API_KEY={os.environ.get('API_KEY')}")
    print(f"  after: API_KEY={os.environ.get('API_KEY')}")


def example_nested_overrides() -> None:
    print("\nExample 2: Nested contexts restore correctly")
    print(f"  before: MODE={os.environ.get('MODE')}")
    with env_var("MODE", "outer"):
        print(f"  inside outer: MODE={os.environ.get('MODE')}")
        with env_var("MODE", "inner"):
            print(f"  inside inner: MODE={os.environ.get('MODE')}")
        print(f"  back to outer: MODE={os.environ.get('MODE')}")
    print(f"  after: MODE={os.environ.get('MODE')}")


def example_multiple_keys() -> None:
    print("\nExample 3: Managing multiple keys independently")
    print(f"  before: USER={os.environ.get('USER')} | REGION={os.environ.get('REGION')}")
    with env_var("USER", "demo-user"):
        with env_var("REGION", "eu-central"):
            print(
                f"  inside: USER={os.environ.get('USER')} | REGION={os.environ.get('REGION')}"
            )
    print(
        f"  after: USER={os.environ.get('USER')} | REGION={os.environ.get('REGION')}"
    )


def example_exception_handling() -> None:
    print("\nExample 4: Cleanup still occurs when exceptions are raised")
    print(f"  before: TEMP_FLAG={os.environ.get('TEMP_FLAG')}")
    try:
        with env_var("TEMP_FLAG", "set-during-block"):
            print(f"  inside: TEMP_FLAG={os.environ.get('TEMP_FLAG')}")
            raise RuntimeError("simulated failure inside context")
    except RuntimeError as exc:
        print(f"  caught: {exc}")
    print(f"  after: TEMP_FLAG={os.environ.get('TEMP_FLAG')}")


def real_world_scenario() -> None:
    print("\nExample 5: Realistic pattern for temporary configuration")

    def simulate_service_call() -> str:
        # Pretend we read env for configuration inside the function
        return f"service uses ENDPOINT={os.environ.get('ENDPOINT')}"

    print(f"  before: ENDPOINT={os.environ.get('ENDPOINT')}")
    with env_var("ENDPOINT", "https://staging.example.com"):
        print("  inside staging: " + simulate_service_call())
    print("  back to default: " + simulate_service_call())


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING STATE CONTEXT MANAGERS")
    print("=" * 70)

    example_basic_state_flip()
    example_nested_overrides()
    example_multiple_keys()
    example_exception_handling()
    real_world_scenario()

    print("\nAll state context examples completed. State is restored after each block.")


if __name__ == "__main__":
    run_all()
