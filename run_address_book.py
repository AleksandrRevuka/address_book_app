"""
The AddressBookApp module provides an application for managing an address book.

The module defines the `AddressBookApp` class, which extends the `npyscreen.NPSAppManaged` class
and provides functionality for creating and running the address book application.
"""

import npyscreen

from my_address_book.constants import FILE_AB, FILE_NB
from my_address_book.address_book import AddressBook as AB
from my_address_book.notes_book import NotesBook as NB
from my_address_book.theme import MyThemeApp
from my_address_book.menu_forms_AB import EditContactForm, DeleteContactForm, AddContactForm
from my_address_book.menu_forms_NB import EditNoteForm, DeleteNoteForm, AddNoteForm
from my_address_book.main_form_AB import MainFormAB
from my_address_book.main_form_NB import MainFormNB


class AddressBookApp(npyscreen.NPSAppManaged):
    """
    AddressBookApp is an application for managing an address book.

    This class extends the npyscreen.NPSAppManaged class, which provides a framework for building 
    console-based applications using npyscreen library.

    Attributes:
        addressbook (AB): An instance of the AB class, representing the address book.

    Methods:
        __init__: Initializes the AddressBookApp object.
        onStart: Called when the application starts, sets up the theme, reads records from a file, 
        and adds forms to the application.
    """

    def __init__(self) -> None:
        super().__init__()
        self.addressbook = AB()
        self.notesbook = NB()

    def onStart(self) -> None:
        """
        The onStart function is called when the application starts.
        It sets up the theme, reads records from a file, and adds forms to the application.
        """
        npyscreen.setTheme(MyThemeApp)

        self.addressbook.read_records_from_file(FILE_AB)
        
        self.notesbook.read_records_from_file(FILE_NB)

        self.addForm('MAIN', MainFormAB, name='Addressbook',
                     lines=42, columns=130, draw_line=10)
        self.addForm('ADD CONTACT', AddContactForm, name='Add contact',
                     lines=40, columns=65, draw_line=1)
        self.addForm('EDIT CONTACT', EditContactForm, name='Edit contact',
                     lines=10, columns=50, draw_line=1)
        self.addForm('DELETE CONTACT', DeleteContactForm, name='Delete contact',
                     lines=10, columns=50, draw_line=1)
        
        self.addForm("NOTE MAIN", MainFormNB, name='Notesbook',
                     lines=42, columns=130, draw_line=10)
        self.addForm('ADD NOTE', AddNoteForm, name='Add note',
                     lines=40, columns=65, draw_line=1)
        self.addForm("EDIT NOTE", EditNoteForm, name='Edit note',
                     lines=10, columns=50, draw_line=1)
        self.addForm('DELETE NOTE', DeleteNoteForm, name='Delete note',
                     lines=10, columns=50, draw_line=1)

if __name__ == "__main__":
    AddressBookApp().run()
