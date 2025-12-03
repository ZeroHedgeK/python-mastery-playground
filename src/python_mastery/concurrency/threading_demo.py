"""
Threading Demo (I/O Bound)
=========================

Threads are lightweight and share memory.
However, due to the Global Interpreter Lock (GIL), only one thread executes Python bytecode at a time.
This makes them ideal for I/O bound tasks (waiting for network, disk, user input) where the GIL is released.
"""

import threading
import time
import concurrent.futures

def download_file(file_id):
    """Simulates downloading a file (I/O bound task)."""
    print(f"Thread-{file_id}: Starting download...")
    time.sleep(0.5)  # Simulate network latency
    print(f"Thread-{file_id}: Download complete!")
    return f"file_{file_id}.dat"

def demonstrate_threading():
    print("\n=== Threading (I/O Bound) ===")

    start_time = time.perf_counter()

    # Old way: Manually creating threads
    # threads = []
    # for i in range(5):
    #     t = threading.Thread(target=download_file, args=(i,))
    #     threads.append(t)
    #     t.start()
    # for t in threads:
    #     t.join()

    # Modern way: ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        print("Submitting 5 download tasks to pool of 3 workers...")
        results = list(executor.map(download_file, range(5)))

    elapsed = time.perf_counter() - start_time
    print(f"All downloads finished in {elapsed:.2f}s")
    print(f"Results: {results}")

    # Note: 5 tasks * 0.5s = 2.5s sequential work.
    # With 3 workers, it should take approx 1.0s (2 batches).

if __name__ == "__main__":
    demonstrate_threading()

