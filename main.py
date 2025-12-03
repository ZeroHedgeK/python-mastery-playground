"""
main.py - Main entry point for running all examples and tests.

This script provides a menu system to run individual decorator examples
or all tests. It makes it easy to explore each decorator separately.
"""

import subprocess
import sys


def run_timer_examples():
    """Run the timer examples."""
    print("\n" + "=" * 70)
    print("RUNNING @timer EXAMPLES")
    print("=" * 70)
    subprocess.run([sys.executable, "timer_examples.py"])


def run_retry_examples():
    """Run the retry examples."""
    print("\n" + "=" * 70)
    print("RUNNING @retry EXAMPLES")
    print("=" * 70)
    subprocess.run([sys.executable, "retry_examples.py"])


def run_rate_limit_examples():
    """Run the rate limit examples."""
    print("\n" + "=" * 70)
    print("RUNNING @rate_limit EXAMPLES")
    print("=" * 70)
    subprocess.run([sys.executable, "rate_limit_examples.py"])


def run_cache_examples():
    """Run the cache examples."""
    print("\n" + "=" * 70)
    print("RUNNING @cache EXAMPLES")
    print("=" * 70)
    subprocess.run([sys.executable, "cache_examples.py"])


def run_all_examples():
    """Run all examples in sequence."""
    print("\n" + "=" * 70)
    print("RUNNING ALL EXAMPLES")
    print("=" * 70)

    examples = [
        ("Timer Examples", "examples/timer.py"),
        ("Retry Examples", "examples/retry.py"),
        ("Rate Limit Examples", "examples/rate_limit.py"),
        ("Cache Examples", "examples/cache.py"),
    ]

    for name, filename in examples:
        print(f"\n{'=' * 70}")
        print(f"RUNNING {name.upper()}")
        print("=" * 70)
        subprocess.run([sys.executable, filename])


def run_tests():
    """Run all unit tests."""
    print("\n" + "=" * 70)
    print("RUNNING ALL TESTS")
    print("=" * 70)
    subprocess.run([sys.executable, "tests/test_decorators.py"])


def show_menu():
    """Display the main menu."""
    print("\n" + "=" * 70)
    print("PYTHON DECORATORS LEARNING PROJECT")
    print("=" * 70)
    print()
    print("This project demonstrates four practical Python decorators:")
    print("  1. @timer       - Logs execution time")
    print("  2. @retry       - Retries failed functions")
    print("  3. @rate_limit  - Throttles function calls")
    print("  4. @cache       - Caches results with expiration")
    print()
    print("Each decorator is explained line-by-line in the code.")
    print("=" * 70)
    print()
    print("MENU:")
    print("  1. Run @timer examples")
    print("  2. Run @retry examples")
    print("  3. Run @rate_limit examples")
    print("  4. Run @cache examples")
    print("  5. Run ALL examples")
    print("  6. Run tests")
    print("  7. Exit")
    print()


def main():
    """Main function to handle user interaction."""
    while True:
        show_menu()

        try:
            choice = input("Enter your choice (1-7): ").strip()

            if choice == "1":
                run_timer_examples()
            elif choice == "2":
                run_retry_examples()
            elif choice == "3":
                run_rate_limit_examples()
            elif choice == "4":
                run_cache_examples()
            elif choice == "5":
                run_all_examples()
            elif choice == "6":
                run_tests()
            elif choice == "7":
                print("\nThank you for using the Python Decorators Learning Project!")
                print("Happy coding! 🐍")
                break
            else:
                print("\n❌ Invalid choice. Please enter a number between 1 and 7.")

        except KeyboardInterrupt:
            print("\n\nExiting program. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")


if __name__ == "__main__":
    main()
