import time
import functools

def log_action(func):
    """Decorator: log function calls."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__} with args={args[1:]}, kwargs={kwargs}")
        return func(*args, **kwargs)
    return wrapper

def measure_time(func):
    """Decorator: measure runtime of functions."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"[TIME] {func.__name__} took {elapsed:.2f}s")
        return result
    return wrapper
