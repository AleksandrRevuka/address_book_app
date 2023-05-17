"""error"""

from typing import Callable



def input_error(func):
    """Decorator for handling input errors"""
    def wrapper_input_error(*args: tuple, **kwargs: dict) -> str | bool:
        """Wrapper function for handling input errors"""
        try:
            func(*args, **kwargs)
            return False

        except TypeError as error:
            return f"TypeError: {error}"
  
        except ValueError as error:
            return f"ValueError: {error}"

        except KeyError as error:
            return f"KeyError: {error}"
        
    return wrapper_input_error
