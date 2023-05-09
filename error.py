"""error"""

import sys
import click


def input_error(func):
    """Decorator for handling input errors"""
    def wrraper_input_error(*args, **kwargs):
        """Wrapper function for handling input errors"""
        try:
            func(*args, **kwargs)

        except TypeError as error:
            click.secho(f"TypeError: {error}", fg='red')
            sys.exit('Try again!')

        except ValueError as error:
            click.secho(f"ValueError: {error}", fg='red')
            sys.exit('Try again!')

        except KeyError as error:
            click.secho(f"KeyError: {error}", fg='red')
            sys.exit('Try again!')
        
    return wrraper_input_error
