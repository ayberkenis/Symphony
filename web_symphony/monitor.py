import time
import functools


def timer(func):
    """A decorator that prints the runtime of the decorated function."""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.time_ns()
        start_time_ms = time.time()
        value = func(*args, **kwargs)
        end_time = time.time_ns()
        end_time_ms = time.time()
        run_time = end_time - start_time
        run_time_ms = end_time_ms - start_time_ms
        print(
            f"Finished {func.__name__!r} in {run_time} ns / {run_time_ms} ms"
        )  # Display runtime in nanoseconds
        return value

    return wrapper_timer


class MonitorServer:
    def __init__(self, target_cls) -> None:
        self.target_cls = target_cls
        self.decorate_methods()

    def decorate_methods(self):
        for attr_name in dir(self.target_cls):
            attr = getattr(self.target_cls, attr_name)
            if callable(attr):
                setattr(self.target_cls, attr_name, timer(attr))

    def start(self):
        print("Starting monitor server...")

    def stop(self):
        print("Stopping monitor server...")

    def __repr__(self) -> str:
        return f"<MonitorServer>"

    def __str__(self) -> str:
        return f"MonitorServer"
