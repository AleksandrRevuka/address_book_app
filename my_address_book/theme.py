"""
Theme module provides the MyThemeWidgets class for customizing the appearance of npyscreen widgets.

Classes:
    MyThemeWidgets(npyscreen.ThemeManager):
        A class for defining a custom theme for npyscreen widgets.
"""
import npyscreen


class MyThemeApp(npyscreen.ThemeManager):
    """
    A class for defining a custom theme for npyscreen widgets.

    Inherits from npyscreen.ThemeManager.

    Attributes:
        default_colors (dict): A dictionary defining the default color scheme for different widget elements.
    """

    default_colors = {
        "DEFAULT": "MAGENTA_BLACK",
        "FORMDEFAULT": "YELLOW_BLACK",
        "NO_EDIT": "CYAN_BLACK",
        "STANDOUT": "CYAN_BLACK",
        "CURSOR": "WHITE_BLACK",
        "CURSOR_INVERSE": "BLACK_WHITE",
        "LABEL": "CYAN_BLACK",
        "LABELBOLD": "YELLOW_BLACK",
        "CONTROL": "YELLOW_BLACK",
        "WARNING": "RED_BLACK",
        "CRITICAL": "BLACK_RED",
        "GOOD": "GREEN_BLACK",
        "GOODHL": "GREEN_BLACK",
        "VERYGOOD": "BLACK_GREEN",
        "CAUTION": "YELLOW_BLACK",
        "CAUTIONHL": "BLACK_YELLOW",
    }
