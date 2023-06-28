"""
error module provides the input_error decorator for handling input errors.

Functions:
    input_error(func: Callable[..., Any]) -> Callable[..., str]:
        Decorator for handling input errors.
"""
from typing import Any
from typing import Callable
from typing import Union


def input_error(func: Callable[..., Any]) -> Callable[..., Union[str, Exception]]:
    """
    Decorator for handling input errors
    """

    def wrapper_input_error(*args: tuple) -> Union[str, Exception]:
        """
        Wrapper function for handling input errors
        """
        try:
            func(*args)
            return ""

        except TypeError as error:
            return f"TypeError: {error}"

        except ValueError as error:
            return f"ValueError: {error}"

        except KeyError as error:
            return f"KeyError: {error}"

    return wrapper_input_error
