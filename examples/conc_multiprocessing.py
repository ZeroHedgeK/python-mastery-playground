"""
Multiprocessing examples for CPU-bound work, shared state, and IPC.

Use processes to sidestep the GIL for CPU-heavy tasks. Includes process pools,
Queues for IPC, shared Value/Array, and a pickling gotcha with lambdas.
"""

from __future__ import annotations

import multiprocessing as mp
import time
from concurrent.futures import ProcessPoolExecutor
from python_mastery.concurrency import (
    multiprocessing_demo as _library_reference,
)  # noqa: F401


def cpu_heavy(n: int) -> int:
    # Count primes up to n (simple, CPU-bound)
    def is_prime(x: int) -> bool:
        if x < 2:
            return False
        for i in range(2, int(x**0.5) + 1):
            if x % i == 0:
                return False
        return True

    return sum(1 for i in range(n) if is_prime(i))


def example_cpu_sequential_vs_processes() -> None:
    print("\nExample 1: CPU-bound sequential vs processes")
    inputs = [50_000, 60_000, 55_000, 52_000]

    start = time.perf_counter()
    seq = [cpu_heavy(n) for n in inputs]
    seq_elapsed = time.perf_counter() - start

    start = time.perf_counter()
    with ProcessPoolExecutor() as ex:
        par = list(ex.map(cpu_heavy, inputs))
    par_elapsed = time.perf_counter() - start

    print(f"  sequential: {seq_elapsed:.3f}s -> {seq}")
    print(f"  processes:  {par_elapsed:.3f}s -> {par}")
    print("  Processes should show real speedup on CPU-bound work vs threads.")


def example_shared_value_and_queue() -> None:
    print("\nExample 2: Shared Value/Array and Queue IPC")
    counter = mp.Value("i", 0)
    results: mp.Queue[int] = mp.Queue()

    def worker(n: int, counter: mp.Value, out: mp.Queue[int]) -> None:
        local = cpu_heavy(n)
        with counter.get_lock():
            counter.value += 1
        out.put(local)

    inputs = [20_000, 22_000, 24_000]
    procs = [mp.Process(target=worker, args=(n, counter, results)) for n in inputs]
    for p in procs:
        p.start()
    for p in procs:
        p.join()

    collected = [results.get() for _ in inputs]
    print(f"  completed workers: {counter.value}")
    print(f"  results: {collected}")


def example_pickling_gotcha() -> None:
    print("\nExample 3: Lambdas/closures do not pickle in ProcessPool")
    try:
        with ProcessPoolExecutor() as ex:
            list(ex.map(lambda x: x + 1, [1, 2, 3]))
    except Exception as exc:
        print(f"  expected pickling failure: {type(exc).__name__}: {exc}")

    # Fix: use top-level functions instead of lambdas/closures
    with ProcessPoolExecutor() as ex:
        fixed = list(ex.map(int, ["1", "2", "3"]))
    print(f"  fixed by using top-level callable: {fixed}")


def example_process_pool_map() -> None:
    print("\nExample 4: ProcessPoolExecutor.map for bulk CPU tasks")
    inputs = [30_000, 30_000, 30_000]
    with ProcessPoolExecutor() as ex:
        results = list(ex.map(cpu_heavy, inputs))
    print(f"  results: {results}")


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING MULTIPROCESSING")
    print("=" * 70)

    example_cpu_sequential_vs_processes()
    example_shared_value_and_queue()
    example_pickling_gotcha()
    example_process_pool_map()

    print("\nAll multiprocessing examples completed.")


if __name__ == "__main__":
    mp.freeze_support()
    run_all()
