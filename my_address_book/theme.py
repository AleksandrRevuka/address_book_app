"""Theme"""
import npyscreen


class MyThemeWidgets(npyscreen.ThemeManager):
    """..."""
    default_colors = {
        'DEFAULT': 'MAGENTA_BLACK',
        'FORMDEFAULT': 'YELLOW_BLACK',
        'NO_EDIT': 'CYAN_BLACK',
        'STANDOUT': 'CYAN_BLACK',
        'CURSOR': 'WHITE_BLACK',
        'CURSOR_INVERSE': 'BLACK_WHITE',
        'LABEL': 'CYAN_BLACK',
        'LABELBOLD': 'YELLOW_BLACK',
        'CONTROL': 'YELLOW_BLACK',
        'WARNING': 'RED_BLACK',
        'CRITICAL': 'BLACK_RED',
        'GOOD': 'GREEN_BLACK',
        'GOODHL': 'GREEN_BLACK',
        'VERYGOOD': 'BLACK_GREEN',
        'CAUTION': 'YELLOW_BLACK',
        'CAUTIONHL': 'BLACK_YELLOW',
    }
