"""Theme"""
import npyscreen



class MyThemeWidgets(npyscreen.ThemeManager):
    """..."""
    default_colors = {
        'DEFAULT': 'YELLOW_BLACK',
        'FORMDEFAULT': 'YELLOW_BLACK',
        'NO_EDIT': 'BLUE_BLACK',
        'STANDOUT': 'CYAN_BLACK',
        'CURSOR': 'WHITE_BLACK',
        'CURSOR_INVERSE': 'BLACK_WHITE',
        'LABEL': 'BLUE_BLACK',
        'LABELBOLD': 'YELLOW_BLACK',
        'CONTROL': 'GREEN_BLACK',
        'WARNING': 'RED_BLACK',
        'CRITICAL': 'BLACK_RED',
        'GOOD': 'GREEN_BLACK',
        'GOODHL': 'GREEN_BLACK',
        'VERYGOOD': 'BLACK_GREEN',
        'CAUTION': 'YELLOW_BLACK',
        'CAUTIONHL': 'BLACK_YELLOW',
    }