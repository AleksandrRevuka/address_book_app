"""..."""
from abc import ABCMeta, abstractmethod
import npyscreen


class IMainForm(npyscreen.FormBaseNewWithMenus, metaclass=ABCMeta):
    """..."""

    @abstractmethod
    def close_menu(self) -> None:
        pass

    @abstractmethod
    def exit(self) -> None:
        pass

    @abstractmethod
    def on_ok(self) -> None:
        pass


class MainForm(IMainForm):
    """
    MainFormStorage is the main form of the application.

    Attributes:
        print_contacts_widget (npyscreen.TitlePager): Widget to display the list of contacts.
        search_widget (npyscreen.TitleText): Widget for searching contacts.
        menu (npyscreen.Menu): Menu object for accessing various options.

    Methods:
        close_menu: Closes the menu.
        exit: Exits the program.
        on_ok: Called when the user presses OK on a form, closes all forms and exits.
    """

    def close_menu(self) -> None:
        """
        The close_menu function is a function that closes the menu.
        """
        self.parentApp.setNextFormPrevious()

    def exit(self) -> None:
        """
        The exit function is used to exit the program.
        """
        self.on_ok()

    def on_ok(self) -> None:
        """
        The on_ok function is called when the user presses OK on a form.
        It will call the switchForm method of the parentApp, passing None as an argument.
        This tells npyscreen to close all forms and exit.
        """
        self.parentApp.switchForm(None)
