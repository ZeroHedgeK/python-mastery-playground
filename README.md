# Python Decorators Learning Project

A comprehensive learning project that demonstrates four practical Python decorators with detailed line-by-line explanations.

## 📚 Project Structure

```
.
├── decorators/           # Decorator package
│   ├── __init__.py      # Package initialization
│   ├── timer.py         # @timer decorator
│   ├── retry.py         # @retry decorator
│   ├── rate_limit.py    # @rate_limit decorator
│   └── cache.py         # @cache decorator
├── examples/            # Example scripts
│   ├── timer.py         # @timer examples
│   ├── retry.py         # @retry examples
│   ├── rate_limit.py    # @rate_limit examples
│   └── cache.py         # @cache examples
├── tests/               # Unit tests
│   └── test_decorators.py
├── main.py              # Interactive menu
├── README.md            # This file
├── setup.cfg           # Package configuration
└── plan.md             # Project planning
```

## 🎯 Decorators Included

### 1. @timer

Logs the execution time of functions. Perfect for performance monitoring.

```python
from decorators import timer

@timer
def slow_function():
    time.sleep(1)
    return "Done"
```

### 2. @retry

Automatically retries failed functions with configurable attempts and delays.

```python
from decorators import retry

@retry(max_attempts=3, delay=1.0)
def unreliable_api_call():
    # Might fail sometimes
    return "Success"
```

### 3. @rate_limit

Throttles function calls to prevent exceeding rate limits.

```python
from decorators import rate_limit

@rate_limit(calls=5, period=60)  # 5 calls per minute
def api_endpoint():
    return "API response"
```

### 4. @cache

Caches function results with time-to-live expiration.

```python
from decorators import cache

@cache(ttl=300)  # Cache for 5 minutes
def expensive_computation(n):
    return n * n * n
```

## 🚀 How to Use

### Interactive Menu (Recommended)

```bash
python main.py
```

### Individual Examples

```bash
python examples/timer.py      # Learn @timer
python examples/retry.py      # Learn @retry
python examples/rate_limit.py # Learn @rate_limit
python examples/cache.py      # Learn @cache
```

### Run Tests

```bash
python tests/test_decorators.py
```

## 📖 Learning Path

1. **Start with the interactive menu**: Run `python main.py` to see all decorators in action
2. **Study individual decorators**: Read the implementation files in `decorators/`
3. **Run focused examples**: Use the example scripts to understand each decorator
4. **Read the tests**: See how each decorator is tested and what edge cases are covered

## 🎓 Key Concepts Covered

- Decorator basics and syntax
- `functools.wraps` for preserving metadata
- Closure and variable capture
- Higher-order functions
- Error handling and retry logic
- Thread safety with locks
- Caching strategies
- Rate limiting algorithms

## 🔧 Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## 📄 License

This project is created for educational purposes. Feel free to use and modify as needed for learning.
