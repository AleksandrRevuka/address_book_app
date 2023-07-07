"""
error module provides the input_error decorator for handling input errors.

Functions:
    input_error(func: Callable[..., Any]) -> Callable[..., str]:
        Decorator for handling input errors.
"""
from typing import Any
from typing import Callable


def input_error(func: Callable[..., Any]) -> Callable[..., str]:
    """
    Decorator for handling input errors
    """

    def wrapper_input_error(*args: tuple) -> str:
        """
        Wrapper function for handling input errors
        """
        try:
            result = func(*args)
            return result

        except TypeError as error:
            return f"TypeError: {error}"

        except ValueError as error:
            return f"ValueError: {error}"

        except KeyError as error:
            return f"KeyError: {error}"

        except PermissionError as error:
            return f"PermissionError: {error}"

        except FileNotFoundError as error:
            return f"FileNotFoundError: {error}"

        except RuntimeError as error:
            return f"RuntimeError: {error}"

    return wrapper_input_error
