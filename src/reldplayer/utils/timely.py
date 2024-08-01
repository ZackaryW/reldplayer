import time
from functools import wraps

class timelyprop:
    def __init__(self, timeout: int):
        self.timeout = timeout

    def __call__(self, func):
        attr_name = f"_{func.__name__}_cache"
        time_name = f"_{func.__name__}_time"

        @property
        @wraps(func)
        def wrapper(instance):
            current_time = time.time()

            # Check if the cached value is present and still valid
            if (not hasattr(instance, attr_name) or
                current_time - getattr(instance, time_name, 0) >= self.timeout):
                # Calculate and cache the new value
                value = func(instance)
                setattr(instance, attr_name, value)
                setattr(instance, time_name, current_time)

            # Return the cached value
            return getattr(instance, attr_name)

        return wrapper

def timely(timeout: int):
    def decorator(func):
        cache = {}
        timestamp = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal cache, timestamp
            current_time = time.time()
            key = (args, frozenset(kwargs.items()))

            # Check if the result is cached and still valid
            if key in cache and current_time - timestamp[key] < timeout:
                return cache[key]

            # Calculate the new result and cache it
            result = func(*args, **kwargs)
            cache[key] = result
            timestamp[key] = current_time
            return result

        return wrapper
    return decorator