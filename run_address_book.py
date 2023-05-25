"""run menu"""

import npyscreen

from my_address_book.constants import FILE
from my_address_book.address_book import AddressBook as AB
from my_address_book.theme import MyThemeWidgets
from my_address_book.menu_forms import EditContactForm, DeleteContactForm, AddContactForm
from my_address_book.main_form import MainForm


class AddressBookApp(npyscreen.NPSAppManaged):
    """..."""

    def __init__(self) -> None:
        super().__init__()
        self.addressbook = AB()

    def onStart(self) -> None:
        """
        The onStart function is called when the application starts.
        It sets up the theme, reads records from a file, and adds forms to the application.
        """
        npyscreen.setTheme(MyThemeWidgets)

        self.addressbook.read_records_from_file(FILE)

        self.addForm('MAIN', MainForm, name='Addressbook',
                     lines=42, columns=130, draw_line=10)
        self.addForm('ADD CONTACT', AddContactForm, name='Add contact',
                     lines=40, columns=65, draw_line=1)
        self.addForm('EDIT CONTACT', EditContactForm, name='Edit contact',
                     lines=20, columns=50, draw_line=1)
        self.addForm('DELETE CONTACT', DeleteContactForm, name='Delete contact',
                     lines=10, columns=50, draw_line=1)


if __name__ == "__main__":
    AddressBookApp().run()
