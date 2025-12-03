"""
Context Manager Usage Examples
=============================

This module demonstrates practical usage of the Timer context manager
with both class-based and decorator-based approaches.
"""

import time

from python_mastery.context_managers import Timer, timer_context


def demonstrate_class_based_timer():
    """Demonstrate the class-based Timer context manager."""
    print("=== Class-based Timer Examples ===\n")

    # Example 1: Basic timing
    print("1. Basic timing with elapsed time access:")
    with Timer() as timer:
        time.sleep(0.1)  # Simulate work
        print(f"   Work in progress... (elapsed so far: {timer.elapsed:.4f}s)")

    print(f"   Final elapsed time: {timer.elapsed:.4f}s\n")

    # Example 2: Named timer
    print("2. Named timer for better identification:")
    with Timer("database_query"):
        time.sleep(0.05)
        print("   Database query executed")

    # Example 3: Multiple timers
    print("\n3. Multiple timers in sequence:")
    with Timer("data_loading") as load_timer:
        time.sleep(0.03)

    with Timer("data_processing") as process_timer:
        time.sleep(0.07)

    with Timer("data_saving") as save_timer:
        time.sleep(0.02)

    total_time = load_timer.elapsed + process_timer.elapsed + save_timer.elapsed
    print(f"   Total pipeline time: {total_time:.4f}s")

    # Example 4: Timer with exception
    print("\n4. Timer behavior with exceptions:")
    try:
        with Timer("exception_test") as timer:
            time.sleep(0.02)
            raise ValueError("Simulated error")
    except ValueError:
        print(f"   Exception caught, but timer still recorded: {timer.elapsed:.4f}s")


def demonstrate_decorator_based_timer():
    """Demonstrate the @contextmanager decorator-based timer."""
    print("\n\n=== @contextmanager Decorator Examples ===\n")

    # Example 1: Basic usage
    print("1. Simple timing:")
    with timer_context():
        time.sleep(0.05)
        print("   Task completed")

    # Example 2: Named timer
    print("\n2. Named timer:")
    with timer_context("file_processing"):
        time.sleep(0.03)
        print("   File processed")

    # Example 3: Nested contexts
    print("\n3. Nested timer contexts:")
    with timer_context("outer_operation"):
        time.sleep(0.02)
        print("   Outer work")

        with timer_context("inner_operation"):
            time.sleep(0.03)
            print("   Inner work")

        time.sleep(0.01)
        print("   More outer work")


def demonstrate_practical_use_cases():
    """Demonstrate practical use cases for timing."""
    print("\n\n=== Practical Use Cases ===\n")

    # Use case 1: Function performance monitoring
    print("1. Monitoring function performance:")

    def process_data(data_size):
        with Timer(f"process_{data_size}_items"):
            # Simulate data processing
            time.sleep(data_size * 0.01)
            return f"Processed {data_size} items"

    result1 = process_data(5)
    result2 = process_data(10)
    print(f"   Results: {result1}, {result2}")

    # Use case 2: API call timing
    print("\n2. API call timing:")

    def simulate_api_call(endpoint):
        with Timer(f"API_{endpoint}"):
            # Simulate network delay
            time.sleep(0.05)
            return {"status": "success", "endpoint": endpoint}

    response = simulate_api_call("users")
    print(f"   API response: {response}")

    # Use case 3: Database transaction timing
    print("\n3. Database transaction simulation:")
    with Timer("transaction"):
        # Simulate transaction steps
        with Timer("  - connection"):
            time.sleep(0.01)

        with Timer("  - query_execution"):
            time.sleep(0.03)

        with Timer("  - result_processing"):
            time.sleep(0.02)

        print("   Transaction completed")


def compare_approaches():
    """Compare the two timer approaches side by side."""
    print("\n\n=== Approach Comparison ===\n")

    print("Class-based Timer advantages:")
    print("• Can access timing data during execution")
    print("• Can maintain state and provide methods")
    print("• Better for complex resource management")
    print("• More explicit and easier to debug")

    print("\n@contextmanager advantages:")
    print("• More concise and Pythonic")
    print("• Easier to write for simple cases")
    print("• Less boilerplate code")
    print("• Natural flow with generator syntax")

    print("\nWhen to use each:")
    print("• Use class-based when you need to:")
    print("  - Access context data during execution")
    print("  - Implement complex resource management")
    print("  - Provide additional methods")
    print("  - Need fine-grained control over exceptions")
    print("\n• Use @contextmanager when you:")
    print("  - Just need simple setup/cleanup")
    print("  - Don't need to access context data")
    print("  - Want concise, readable code")
    print("  - Are doing straightforward resource management")


if __name__ == "__main__":
    demonstrate_class_based_timer()
    demonstrate_decorator_based_timer()
    demonstrate_practical_use_cases()
    compare_approaches()
