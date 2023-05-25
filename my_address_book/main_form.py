"""main form"""

import npyscreen

from my_address_book.utils import print_all_contacts
from my_address_book.validation import criteria_validation
from my_address_book.address_book import AddressBook as AB


class MainForm(npyscreen.FormBaseNewWithMenus):
    """..."""

    def create(self) -> None:
        """
        The create function is called when the form is created.
        It sets up the widgets and their initial values.
        """

        self.print_contacts_widget = self.add(npyscreen.TitlePager, name="Contacts:", begin_entry_at=9, max_height=36)
        self.search_widget = self.add(npyscreen.TitleText, name="Search:", rely=39, begin_entry_at=10)
        self.search_widget.when_cursor_moved = self.while_editing

        self.menu = self.new_menu(name="Menu", shortcut="m")
        self.menu.addItem("Add contact", self.add_contact, "1")
        self.menu.addItem("Edit contact", self.edit_contact, "2")
        self.menu.addItem("Delete contact", self.delete_contact, "3")
        self.menu.addItem("Close Menu", self.close_menu, "^X")
        self.menu.addItem("Exit", self.exit, "^E")

    def while_editing(self, *args: list, **kwargs: dict) -> None:
        if self.search_widget.value:
            criteria = self.search_widget.value.lower()
            message = criteria_validation(criteria)
            if message:
                npyscreen.notify_confirm(message, "Warning!", editw=1)
                self.search_widget.value = ''
                self.update_list(self.parentApp.addressbook)

            result = self.parentApp.addressbook.search(criteria)
            if isinstance(result, AB):
                self.update_list(result)
            else:
                npyscreen.notify_confirm(result, "Warning!", editw=1)
                self.search_widget.value = ''
                self.update_list(self.parentApp.addressbook)
        else:
            self.update_list(self.parentApp.addressbook)

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
        self.print_contacts_widget.values = contacts.split('\n')
        self.print_contacts_widget.display()

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