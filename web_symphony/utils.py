import time
import functools
import logging
import colored
import orjson


def print_red(func):
    """A decorator that prints the runtime of the decorated function."""

    @functools.wraps(func)
    def print_red_wrapper(*args, **kwargs):
        print(colored.Fore.RED)
        value = func(*args, **kwargs)
        print(colored.Style.RESET)
        return value

    return print_red_wrapper


def jsoned(data: dict) -> bytes:
    """This method is used to return a JSON response.

    Args:
        data (dict): Data to be returned
        status (int, optional): Status code of the response. Defaults to 200.

    Returns:
        OutgoingResponse: A response object
    """
    return orjson.loads(data)


def timer(func):
    """A decorator that prints the runtime of the decorated function."""
    logger = logging.getLogger("fortuna")

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):

        start_time = time.time_ns()
        value = func(*args, **kwargs)
        end_time = time.time_ns()
        run_time = end_time - start_time
        logger.info(f"Finished {func.__name__!r} in {run_time} ns")
        return value

    return wrapper_timer
