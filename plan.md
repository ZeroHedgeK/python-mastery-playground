# Python Decorators Learning Project Plan

## Project Overview

This project will teach decorators through hands-on implementation of four practical decorators, starting with @timer.

## Project Structure

```
.
├── decorators.py      # Core decorator implementations
├── examples.py        # Demonstration functions
├── tests.py          # Unit tests
├── main.py           # Runner for examples and tests
└── plan.md           # This plan document
```

## Implementation Strategy

### Phase 1: @timer Decorator

**File: decorators.py**

- Import required modules: functools, time, typing
- Create @timer decorator that:
  - Uses functools.wraps to preserve function metadata
  - Records start time before function execution
  - Executes the original function
  - Records end time after function execution
  - Calculates and logs execution time
  - Returns the function's result

**File: examples.py**

- Create slow_function() that sleeps to demonstrate timing
- Create fast_function() that performs quick operations
- Create compute_sum(n) that calculates sum of numbers

**File: tests.py**

- Test that timer decorator logs execution time
- Test that decorated functions return correct results
- Test that function metadata is preserved

### Phase 2: @retry Decorator

**File: decorators.py**

- Add parameters: max_attempts, delay
- Implement retry logic with try/except
- Add exponential backoff option
- Handle specific exception types

**File: examples.py**

- Create unreliable_function() that fails randomly
- Create network_simulation() that simulates network calls

**File: tests.py**

- Test successful execution on first try
- Test retry on failure
- Test max attempts reached
- Test delay between retries

### Phase 3: @rate_limit Decorator

**File: decorators.py**

- Add parameters: calls, period (in seconds)
- Use threading.Lock for thread safety
- Track call timestamps in a list
- Clean up old timestamps outside the period
- Block or raise exception when limit exceeded

**File: examples.py**

- Create api_call() simulation
- Create multiple rapid calls demonstration

**File: tests.py**

- Test rate limiting enforcement
- Test that calls within limit work
- Test period reset functionality

### Phase 4: @cache Decorator

**File: decorators.py**

- Add parameter: ttl (time to live in seconds)
- Use dictionary to store cached results
- Store timestamp along with cached value
- Check ttl before returning cached result
- Implement cache invalidation

**File: examples.py**

- Create expensive_computation() function
- Create function with different arguments
- Demonstrate cache hit/miss scenarios

**File: tests.py**

- Test caching functionality
- Test ttl expiration
- Test cache with different arguments
- Test cache invalidation

### Phase 5: Integration

**File: main.py**

- Import all examples and tests
- Create menu system to run specific demonstrations
- Add option to run all tests
- Provide clear output formatting

## Key Learning Concepts

1. **Decorator Basics**: Functions that modify other functions
2. **functools.wraps**: Preserves function metadata
3. **Closure**: Decorators capture variables from outer scope
4. **Higher-order Functions**: Functions that take/return functions
5. **Timing**: Using time module for performance measurement
6. **Error Handling**: Try/except for retry logic
7. **Thread Safety**: Using locks for concurrent access
8. **Caching**: Storing and retrieving computed results

## Next Steps

1. Switch to Code mode to implement Phase 1 (@timer)
2. Test the implementation
3. Proceed with subsequent phases
4. Add documentation and examples
5. Create comprehensive tests

## Notes

- All implementations use only Python standard library
- Each decorator will be explained line by line
- Examples will be simple but practical
- Tests will cover normal and edge cases
