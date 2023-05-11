"""error"""

from typing import Callable
import sys
import click



def input_error(func: Callable[..., None]) -> Callable[..., None]:
    """Decorator for handling input errors"""
    def wrapper_input_error(*args: tuple, **kwargs: dict) -> None:
        """Wrapper function for handling input errors"""
        try:
            func(*args, **kwargs)

        except TypeError as error:
            click.secho(f"TypeError: {error}", fg='red', italic=True)
            sys.exit('Try again!')

        except ValueError as error:
            click.secho(f"ValueError: {error}", fg='red', italic=True)
            sys.exit('Try again!')

        except KeyError as error:
            click.secho(f"KeyError: {error}", fg='red', italic=True)
            sys.exit('Try again!')
        
    return wrapper_input_error
