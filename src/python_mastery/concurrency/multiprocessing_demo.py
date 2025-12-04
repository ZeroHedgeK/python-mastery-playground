"""
Multiprocessing Demo (CPU Bound)
===============================

Processes run in separate memory spaces and have their own GIL.
This allows them to run in parallel on multiple CPU cores.
Ideal for CPU-intensive tasks (math, image processing).
"""

import multiprocessing
import os
import time


def heavy_computation(num: int) -> int:
    """Simulate a CPU-intensive task."""
    print(f"Process-{os.getpid()}: Calculating factorial of {num}...")
    result = 1
    for i in range(1, num + 1):
        result *= i
    # Simulate more work
    start = time.time()
    while time.time() - start < 0.5:
        pass
    print(f"Process-{os.getpid()}: Finished {num}!")
    return result


def demonstrate_multiprocessing() -> None:
    """Demonstrate using multiprocessing Pool for CPU-bound tasks."""
    print("\n=== Multiprocessing (CPU Bound) ===")

    cpu_count = multiprocessing.cpu_count()
    print(f"System has {cpu_count} CPUs")

    start_time = time.perf_counter()

    # Create a pool of workers equal to CPU count
    with multiprocessing.Pool(processes=cpu_count) as pool:
        numbers = [50000, 50000, 50000, 50000]
        print(f"Submitting {len(numbers)} heavy tasks...")

        # map blocks until all results are ready
        results = pool.map(heavy_computation, numbers)

    elapsed = time.perf_counter() - start_time
    print(f"All computations finished in {elapsed:.2f}s")

    # Note: In a single-threaded (or threaded with GIL) program,
    # this would take 4 * 0.5s = 2.0s.
    # With multiprocessing, it should take ~0.5-0.6s total.

    # Suppress unused variable warning
    _ = results


if __name__ == "__main__":
    demonstrate_multiprocessing()
