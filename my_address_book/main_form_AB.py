"""
The module provides the MainForm class, which represents the main form of the address book application.

Classes:
    MainForm(npyscreen.FormBaseNewWithMenus):
        The main form of the address book application, displaying the list of contacts and providing menu options.
"""
import npyscreen

from my_address_book.address_book import AddressBook as AB
from my_address_book.interface_main_form import MainForm
from my_address_book.utils import print_all_contacts


class MainFormAB(MainForm):
    """
    MainForm is the main form of the address book application.

    This form displays the list of contacts, allows searching for contacts,
    and provides menu options for adding, editing, and deleting contacts.

    Methods:
        create: Called when the form is created, sets up the widgets and their initial values.
        add_contact: Allows the user to add a contact to the address book.
        edit_contact: Allows the user to edit a contact's information.
        delete_contact: Allows the user to delete a contact from the address book.
        while_editing: Called when editing the search criteria, performs search and updates the contact list.
        search_contact:
        beforeEditing: Called before the form is displayed, updates the list of contacts.
        update_list: Updates the list of contacts in the address book to reflect any changes.
    """

    def create(self) -> None:
        """
        The create function is called when the form is created.
        It sets up the widgets and their initial values.
        """
        self.print_widget = self.add(npyscreen.TitlePager, name="Contacts:", begin_entry_at=9, max_height=36)
        self.search_widget: npyscreen.TitleText = self.add(npyscreen.TitleText, name="Search:", rely=39, begin_entry_at=10)
        self.search_widget.when_value_edited = self.while_editing

        self.menu = self.new_menu(name="Menu", shortcut="m")
        self.menu.addItem("Add contact", self.add_contact, "1")
        self.menu.addItem("Edit contact", self.edit_contact, "2")
        self.menu.addItem("Delete contact", self.delete_contact, "3")
        self.menu.addItem("Notesbook", self.to_notesbook_fotm, "4")
        self.menu.addItem("Close Menu", self.close_menu, "^X")
        self.menu.addItem("Exit", self.exit, "^E")

    def while_editing(self, *args: list, **kwargs: dict) -> None:
        addressbook = self.parentApp.addressbook
        self.search_contact(addressbook)

    def search_contact(self, addressbook: AB) -> None:
        """
        The search_contact function is used to search for a contact in the address book.
        It takes two arguments: self and addressbook. The first argument, self, is an instance of the MainForm class
        that contains all of the widgets on our form. The second argument, addressbook, is an instance of AddressBook
        class that contains all contacts from our database.
        """

        if self.search_widget.value:
            criteria = self.search_widget.value
            searched_contacts = addressbook.search(criteria)
            self.update_list(searched_contacts)
        else:
            self.update_list(addressbook)

    def beforeEditing(self) -> None:
        """
        The beforeEditing function is called before the form is displayed.
        It updates the list of contacts to be displayed in the form.
        """
        addressbook = self.parentApp.addressbook
        self.update_list(addressbook)

    def update_list(self, addressbook: AB) -> None:
        """
        The update_list function updates the list of contacts in the address book to reflect any changes
        that have been made.
        """
        contacts = print_all_contacts(addressbook)
        self.print_widget.values = contacts.split("\n")
        self.print_widget.display()

    def add_contact(self) -> None:
        """
        The add_contact function allows the user to add a contact to their address book.
        The function takes in no parameters and returns nothing. The function is called by pressing the 'Add Contact'
        button on the main menu screen.
        """
        self.parentApp.switchForm("ADD CONTACT")

    def edit_contact(self) -> None:
        """
        The edit_contact function allows the user to edit a contact's information.
        The function takes in self as an argument and returns None. The function then
        switches to the EDIT CONTACT form.
        """
        self.parentApp.switchForm("EDIT CONTACT")

    def delete_contact(self) -> None:
        """
        The delete_contact function allows the user to delete a contact from their address book.
        The function takes in self as an argument and returns None. The function then switches forms
        to the DELETE CONTACT form.
        """
        self.parentApp.switchForm("DELETE CONTACT")

    def to_notesbook_fotm(self) -> None:
        self.parentApp.switchForm("NOTE MAIN")
