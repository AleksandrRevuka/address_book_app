"""error"""

def input_error(func):
    """Decorator for handling input errors"""
    def wrraper_input_error(*args, **kwargs):
        """Wrapper function for handling input errors"""
        try:
            return func(*args, **kwargs)

        except TypeError as error:
            return f"Error: {error}"

        except ValueError as error:
            return f"Error: {error}"

        except KeyError as error:
            return f"Error: {error}"

    return wrraper_input_error