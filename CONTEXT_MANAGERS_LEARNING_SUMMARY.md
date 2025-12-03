# Context Managers Learning Summary

## What are Context Managers?

Context managers are Python objects that manage resources and ensure proper cleanup, typically used with the `with` statement. They automatically handle setup and teardown operations, making code cleaner and more reliable.

## The Timer Context Manager - Two Approaches

We've implemented a `Timer` context manager using two different approaches to demonstrate the key differences:

### 1. Class-Based Approach (`__enter__`/`__exit__`)

**File:** [`context_managers/timer.py`](context_managers/timer.py:16)

```python
class Timer:
    def __init__(self, name=None):
        self.name = name
        self.start_time = None
        self.end_time = None

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self  # Return self to allow attribute access

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        elapsed = self.end_time - self.start_time
        print(f"Timer: {elapsed:.4f} seconds")
        return False  # Propagate exceptions

    @property
    def elapsed(self):
        """Access elapsed time during execution"""
        if self.start_time is None:
            return None
        if self.end_time is None:
            return time.perf_counter() - self.start_time
        return self.end_time - self.start_time
```

**Key Features:**

- **State Access:** Can access `timer.elapsed` during execution
- **Method Support:** Can add additional methods and properties
- **Explicit Control:** Full control over the context management process
- **Exception Handling:** Fine-grained control over exception propagation

### 2. `@contextmanager` Decorator Approach

**File:** [`context_managers/timer.py`](context_managers/timer.py:74)

```python
@contextmanager
def timer_context(name=None):
    start_time = time.perf_counter()

    try:
        yield  # Yield control to the code block
    finally:
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        print(f"Timer: {elapsed:.4f} seconds")
```

**Key Features:**

- **Concise:** Minimal boilerplate code
- **Pythonic:** Uses generator syntax naturally
- **Automatic Cleanup:** `finally` block ensures cleanup always happens
- **Limited Access:** Cannot access timing data during execution

## Key Differences Explained

### 1. **Access to Context Data**

**Class-based:**

```python
with Timer() as timer:
    time.sleep(0.1)
    print(f"Elapsed so far: {timer.elapsed:.4f}s")  # Works!
```

**@contextmanager:**

```python
with timer_context():
    time.sleep(0.1)
    # Cannot access elapsed time here
```

### 2. **Code Complexity**

**Class-based:** More verbose but explicit

- Requires `__init__`, `__enter__`, `__exit__` methods
- More control, better for complex scenarios
- Easier to debug and understand

**@contextmanager:** More concise but limited

- Single function with `yield`
- Less control, better for simple scenarios
- Can be trickier to debug due to generator magic

### 3. **Exception Handling**

**Class-based:** Fine-grained control

```python
def __exit__(self, exc_type, exc_val, exc_tb):
    # Can inspect exception details
    # Return True to suppress, False to propagate
    return False  # Propagate exceptions
```

**@contextmanager:** Automatic with try/finally

```python
try:
    yield
finally:
    # Always executes, even with exceptions
    # Cannot easily suppress exceptions
```

### 4. **Use Cases**

**When to use Class-based:**

- Complex resource management (database connections, file handles)
- Need to access context data during execution
- Require additional methods on the context manager
- Building reusable library code
- Need precise exception control

**When to use @contextmanager:**

- Simple setup/cleanup operations
- Quick prototyping and scripting
- Don't need to access context data
- Readability and conciseness are priorities
- Straightforward resource management

## Practical Examples

### Example 1: Database Connection Management (Class-based)

```python
class DatabaseConnection:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = create_connection(self.connection_string)
        self.cursor = self.connection.cursor()
        return self  # Allow access to connection and cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        return False

    def query(self, sql):
        """Additional method - only possible with class-based"""
        return self.cursor.execute(sql)

# Usage
with DatabaseConnection("postgres://...") as db:
    results = db.query("SELECT * FROM users")  # Can use additional methods
```

### Example 2: Temporary File (Class-based)

```python
class TemporaryFile:
    def __init__(self, suffix=".tmp"):
        self.suffix = suffix
        self.file_path = None

    def __enter__(self):
        import tempfile
        self.file_path = tempfile.mktemp(suffix=self.suffix)
        return self.file_path  # Return the path, not self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import os
        if self.file_path and os.path.exists(self.file_path):
            os.unlink(self.file_path)
        return False

# Usage
with TemporaryFile(".txt") as temp_path:
    with open(temp_path, "w") as f:
        f.write("temporary data")
    # File automatically deleted after block
```

### Example 3: Simple Resource Lock (@contextmanager)

```python
@contextmanager
def resource_lock(resource_id):
    lock = acquire_lock(resource_id)
    try:
        yield  # Resource is locked
    finally:
        release_lock(lock)

# Usage
with resource_lock("database"):
    # Critical section - resource is locked
    update_database()
# Lock automatically released
```

## Running the Examples

To see both timer approaches in action:

```bash
PYTHONPATH=. python examples/context_manager_examples.py
```

This demonstrates:

- Basic timing with both approaches
- Named timers for better identification
- Access to elapsed time during execution (class-based only)
- Exception handling behavior
- Nested contexts
- Practical use cases (API calls, database operations, etc.)

## Summary

Both approaches are valid and useful - choose based on your specific needs:

- **Class-based**: More powerful, flexible, and explicit. Better for complex scenarios and library code.
- **@contextmanager**: More concise and Pythonic. Better for simple scenarios and quick scripting.

The key insight is that context managers are about **resource management** and **guaranteed cleanup**, not just timing. The `Timer` example is educational because it's simple to understand, but the same principles apply to file handling, database connections, network sockets, and any resource that needs proper setup and teardown.

## Files Created

- [`context_managers/timer.py`](context_managers/timer.py) - Timer implementations
- [`context_managers/__init__.py`](context_managers/__init__.py) - Package initialization
- [`examples/context_manager_examples.py`](examples/context_manager_examples.py) - Usage examples
- [`context_managers/README.md`](context_managers/README.md) - Detailed documentation

## Next Steps

Try modifying the examples to:

1. Add a `Timer` that writes to a log file instead of printing
2. Create a context manager for managing a list of temporary files
3. Implement a retry mechanism within a context manager
4. Combine the `Timer` with other decorators from the decorators module
