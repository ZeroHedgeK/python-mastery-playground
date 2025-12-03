"""
State Management Context Managers
================================

Demonstrates using context managers to temporarily modify global state
(like environment variables) and guarantee restoration.
"""

import os
from contextlib import contextmanager

@contextmanager
def env_var(key, value):
    """
    Temporarily set an environment variable.
    Restores the original value (or deletes if it didn't exist) on exit.
    """
    old_value = os.environ.get(key)
    os.environ[key] = value

    print(f"Set ENV['{key}'] = '{value}'")

    try:
        yield
    finally:
        if old_value is None:
            del os.environ[key]
            print(f"Deleted ENV['{key}']")
        else:
            os.environ[key] = old_value
            print(f"Restored ENV['{key}'] to '{old_value}'")

def demonstrate_state_change():
    print(f"Current API_KEY: {os.environ.get('API_KEY')}")

    with env_var("API_KEY", "temp_secret_123"):
        print(f"Inside context: {os.environ.get('API_KEY')}")

        # Nesting works too
        with env_var("API_KEY", "inner_secret"):
            print(f"Inside nested: {os.environ.get('API_KEY')}")

    print(f"After context: {os.environ.get('API_KEY')}")

if __name__ == "__main__":
    demonstrate_state_change()

