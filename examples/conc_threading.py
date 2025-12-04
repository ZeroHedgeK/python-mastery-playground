"""
Threading examples for I/O-bound work, synchronization, and GIL limitations.

Use threads for I/O-bound tasks; they do not speed up CPU-bound workloads due to
the GIL. Includes locks to fix races, events for signaling, and daemon thread
behavior.
"""

from __future__ import annotations

import threading
import time
from concurrent.futures import ThreadPoolExecutor
from python_mastery.concurrency import threading_demo as _library_reference  # noqa: F401


def io_task(duration: float, label: str) -> str:
    time.sleep(duration)
    return f"{label} done after {duration:.2f}s"


def cpu_task(n: int) -> int:
    # Deliberately CPU-bound (sum of squares) to show GIL impact
    return sum(i * i for i in range(n))


def example_io_sequential_vs_threads() -> None:
    print("\nExample 1: I/O-bound sequential vs threaded")
    durations = [0.3, 0.3, 0.3]

    start = time.perf_counter()
    seq_results = [io_task(d, f"seq-{i}") for i, d in enumerate(durations)]
    seq_elapsed = time.perf_counter() - start

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=3) as ex:
        thread_results = list(ex.map(io_task, durations, [f"thr-{i}" for i in range(len(durations))]))
    thr_elapsed = time.perf_counter() - start

    print(f"  sequential: {seq_elapsed:.3f}s → {seq_results}")
    print(f"  threaded:   {thr_elapsed:.3f}s → {thread_results}")
    print("  Threads win for I/O-bound tasks because they overlap waiting.")


def example_gil_cpu_bound() -> None:
    print("\nExample 2: CPU-bound tasks — threads do NOT help (GIL)")
    work_items = [250_000] * 4

    start = time.perf_counter()
    seq = [cpu_task(n) for n in work_items]
    seq_elapsed = time.perf_counter() - start

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as ex:
        thr = list(ex.map(cpu_task, work_items))
    thr_elapsed = time.perf_counter() - start

    print(f"  sequential: {seq_elapsed:.3f}s")
    print(f"  threaded:   {thr_elapsed:.3f}s")
    print("  Expect near-equal or slower threaded time because of the GIL.")


def example_race_condition_and_lock() -> None:
    print("\nExample 3: Race condition vs locked counter")
    counter = 0
    lock = threading.Lock()

    def unsafe_inc(n: int) -> None:
        nonlocal counter
        for _ in range(n):
            counter += 1  # race

    def safe_inc(n: int) -> None:
        nonlocal counter
        for _ in range(n):
            with lock:
                counter += 1

    target = 10_000
    counter = 0
    threads = [threading.Thread(target=unsafe_inc, args=(target,)) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"  unsafe counter expected {target*4}, got {counter}")

    counter = 0
    threads = [threading.Thread(target=safe_inc, args=(target,)) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"  locked counter expected {target*4}, got {counter}")


def example_event_signaling() -> None:
    print("\nExample 4: Threading.Event for signaling")
    event = threading.Event()

    def worker(name: str) -> None:
        print(f"  {name} waiting for signal...")
        event.wait()
        print(f"  {name} received signal")

    t = threading.Thread(target=worker, args=("worker-1",))
    t.start()
    time.sleep(0.1)
    print("  main sets event")
    event.set()
    t.join()


def example_daemon_vs_non_daemon() -> None:
    print("\nExample 5: Daemon vs non-daemon threads")

    def background():
        for i in range(3):
            time.sleep(0.2)
            print(f"  daemon working {i}")

    def foreground():
        time.sleep(0.3)
        print("  foreground complete")

    daemon_thread = threading.Thread(target=background, daemon=True)
    fg_thread = threading.Thread(target=foreground, daemon=False)
    daemon_thread.start()
    fg_thread.start()
    fg_thread.join()
    print("  main exits; daemon may not finish if still running")


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING THREADING")
    print("=" * 70)

    example_io_sequential_vs_threads()
    example_gil_cpu_bound()
    example_race_condition_and_lock()
    example_event_signaling()
    example_daemon_vs_non_daemon()

    print("\nAll threading examples completed.")


if __name__ == "__main__":
    run_all()
