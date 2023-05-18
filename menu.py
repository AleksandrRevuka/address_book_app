
from datetime import datetime
import npyscreen


from utils import sanitize_phone_number
from validation import (
    name_validation,
    phone_validation,
    email_validation,
    birthday_date_validation,
    criteria_validation,
    check_name_in_address_book,
    check_name_not_in_address_book,
    check_phone_number_in_address_book,
    check_phone_number_not_in_address_book,
    check_email_in_address_book,
    check_email_not_in_address_book,
)
from run_bot import print_all_contacts
from constants import FILE
from address_book import Record, AddressBook as AB
from entities import Phone, User, Email


class EditContactForm(npyscreen.ActionPopup):
    """..."""

    def create(self) -> None:
        """
        The create function is called when the form is created.
        It sets up the widgets and their initial values.
        """
        self.contact_name_for_change = self.add(npyscreen.TitleText, name='Name')

    def beforeEditing(self) -> None:
        """
        The beforeEditing function is called before the form is displayed.
        It allows you to set up the form, and populate it with data from your object.
        The function takes no arguments, but has access to all of the widgets on your form.
        """
        self.contact_name_for_change.value = None

    def check_name(self) -> bool:
        """
        The check_name function checks to see if the name entered by the user is in
        the address book. If it is, then a message will be displayed and the user will
        be prompted to enter another name.
        """
        name = self.contact_name_for_change.value
        message = check_name_not_in_address_book(self.parentApp.addressbook, name)
        if message:
            npyscreen.notify_confirm(message)
            self.contact_name_for_change.value = None
            return False
        return True

    def on_ok(self) -> None:
        """
        The on_ok function is called when the user presses enter on the form.
        It checks if a contact name has been entered, and if so, it passes that value to
        the ADD CONTACT form and switches to that form.
        """
        respon = self.check_name()
        if respon:
            self.parentApp.getForm('ADD CONTACT').value = self.contact_name_for_change.value
            self.parentApp.switchForm('ADD CONTACT')

    def on_cancel(self) -> None:
        """
        The on_cancel function is called when the user presses ^C or ^Q.
        It switches back to the MAIN form.
        """
        self.parentApp.switchForm("MAIN")


class DeleteContactForm(npyscreen.ActionPopup):
    """..."""

    def create(self) -> None:
        """
        The create function is called when the form is created.
        It sets up the widgets and their initial values.
        """
        self.contact_name_for_del = self.add(npyscreen.TitleText, name='Name')

    def beforeEditing(self) -> None:
        """
        The beforeEditing function is called before the form is displayed.
        It allows you to set up the form, and populate it with data from your object.
        The function takes no arguments, but has access to all of the widgets on your form.
        """
        self.contact_name_for_del.value = None

    def check_name(self) -> bool:
        """
        The check_name function is used to check if the name entered by the user
        is in the address book. If it is not, then a message will be displayed and
        the user will be prompted to enter another name.
        """

        name = self.contact_name_for_del.value
        message = check_name_not_in_address_book(self.parentApp.addressbook, name)
        if message:
            npyscreen.notify_confirm(message)
            self.contact_name_for_del.value = None
            return False
        return True

    def delete_contact(self) -> str:
        """
        The delete_contact function is called when the user presses the 'Delete Contact' button.
        It deletes a contact from the address book, and saves it to file.
        """
        self.parentApp.addressbook.delete_record(self.contact_name_for_del.value)
        self.parentApp.addressbook.save_records_to_file(FILE)
        return f"The contact '{self.contact_name_for_del.value.title()}' has been deleted."

    def on_ok(self) -> None:
        """
        The on_ok function is called when the user presses enter on a form.
        It checks to see if the name entered by the user exists in our address book, and if it does, it deletes that contact from our address book.
        If not, then an error message is displayed.
        """
        respon = self.check_name()
        if respon:
            message = self.delete_contact()
            npyscreen.notify_confirm(message, "Delete!", editw=1)

            self.parentApp.switchForm("MAIN")

    def on_cancel(self) -> None:
        """
        The on_cancel function is called when the user presses ^C or ^Q.
        It will return to the previous form, which in this case is MAIN.
        """
        self.parentApp.switchForm("MAIN")


class AddContactForm(npyscreen.ActionForm):
    """..."""

    def create(self) -> None:
        """
        The create function is called when the form is created.
        It sets up the widgets and their initial values.
        """
        self.value = None
        self.contact_name = self.add(npyscreen.TitleText, name='Name')
        self.contact_phone = self.add(npyscreen.TitleText, name='Number phone')
        self.phone_assignment = self.add(npyscreen.TitleSelectOne,
                                         scroll_exit=True,
                                         max_height=4,
                                         name='Phone assignment',
                                         values=['mobile',
                                                 'home',
                                                 'work'
                                                 ])
        self.contact_email = self.add(npyscreen.TitleText, name='Email')
        self.email_assignment = self.add(npyscreen.TitleSelectOne,
                                         scroll_exit=True,
                                         max_height=3,
                                         name='Email assignment',
                                         values=['home',
                                                 'work'
                                                 ])

        self.contact_birth_text = self.add(npyscreen.TitleText, name='Year Birth:')
        self.contact_birth = self.add(npyscreen.TitleDateCombo, name='Date Birth:', date_format='%d-%m-%Y',)
        self.contact_birth.when_parent_changes_value = self.while_editing

    def beforeEditing(self) -> None:
        """
        The beforeEditing function is called before the form is displayed.
        It allows you to set up the form, and populate it with data from your object.
        The self argument refers to the Form itself, not a widget on it.
        """
        if self.value:
            record_contact = self.parentApp.addressbook.get_contact(self.value)

            self.contact_name.value = record_contact.user.name
            self.contact_phone.value = record_contact.phone_numbers[0].subrecord.phone if record_contact.phone_numbers[0].subrecord.phone else ''
            self.phone_assignment.value = record_contact.phone_numbers[0].name
            self.contact_email.value = record_contact.emails[0].subrecord.email if record_contact.emails[0].subrecord.email else ''
            self.email_assignment.value = record_contact.emails[0].name
            self.contact_birth.value = record_contact.user.birthday_date

    def afterEditing(self) -> None:
        """
        The afterEditing function is called after the user has finished editing a form.
        It allows you to perform any actions that are required, such as updating the database with new values.
        The function takes one argument: self, which is a reference to the form itself.
        """
        self.value = None
        self.contact_name.value = None
        self.contact_phone.value = None
        self.phone_assignment.value = None
        self.contact_email.value = None
        self.email_assignment.value = None
        self.contact_birth_text.value = None
        self.contact_birth.value = None

    def data_validation(self) -> bool:
        """
        The data_validation function checks the validity of the data entered by
        the user. It returns True if all data is valid, and False otherwise.
        """

        name = self.contact_name.value
        message = name_validation(name)
        if message:
            npyscreen.notify_confirm(message)
            self.contact_name.clear()
            return False

        if self.value != name:
            message = check_name_in_address_book(self.parentApp.addressbook, name)
            if message:
                npyscreen.notify_confirm(message)
                self.contact_name.value = None
                return False

        if self.contact_phone.value:
            phone = self.contact_phone.value
            phone = sanitize_phone_number(phone)
            message = phone_validation(phone)
            self.contact_phone.value = phone

        if message:
            npyscreen.notify_confirm(message)
            self.contact_phone.value = None
            return False

        if self.contact_email.value:
            email = self.contact_email.value
            message = email_validation(email)
        if message:
            npyscreen.notify_confirm(message)
            self.contact_email.value = None
            return False

        birthday = self.contact_birth.value
        message = birthday_date_validation(birthday)
        if message:
            npyscreen.notify_confirm(message)
            self.contact_birth.value = None
            return False

        return True

    def while_editing(self, *args: list, **kwargs: dict) -> None:
        """
        The while_editing function is a function that allows the user to enter in a year for their birthday, 
        and then it will automatically convert it into the date format.
        """
        if self.contact_birth_text.value:
            if self.contact_birth.value is None:
                birthday = datetime.strptime(str(int(self.contact_birth_text.value)), '%Y').date()
                self.contact_birth.value = birthday

    def add_contact(self) -> str:
        """
        The add_contact function takes the user input from the AddContactForm and
        creates a new contact object. It then adds that contact to the address book,
        and saves it to file.
        """

        email = Email(self.contact_email.value)
        phone = Phone(self.contact_phone.value)
        user = User(self.contact_name.value)
        contact = Record(user)
        contact.add_phone_number(phone, self.phone_assignment.value)
        contact.add_email(email, self.email_assignment.value)
        contact.add_birthday(self.contact_birth.value)

        self.parentApp.addressbook.add_record(contact)
        self.parentApp.addressbook.save_records_to_file(FILE)
        return f"The contact '{self.contact_name.value.title()}' has been added"

    def change_contact(self) -> str:
        """
        The function first deletes the selected contact, then calls add_contact() to create a new one with updated information.
        """
        self.parentApp.addressbook.delete_record(self.value)
        message = self.add_contact()
        message = f"The contact '{self.contact_name.value.title()}' has been updated"
        return message

    def on_ok(self) -> None:
        """
        The on_ok function is called when the user presses OK on the form.
        It checks if all of the fields are valid, and then either adds a new contact or updates an existing one.
        If it's a new contact, it calls add_contact() to create a new record in AddressBook with all of its information; 
        if it's an existing contact, change_contact() is called instead.
        """
        respon = self.data_validation()
        if respon:
            if not self.value:
                message = self.add_contact()
                npyscreen.notify_confirm(message, "Saved!", editw=1)
                self.parentApp.switchForm("MAIN")

            else:
                message = self.change_contact()
                npyscreen.notify_confirm(message, "Saved!", editw=1)

            self.parentApp.switchForm("MAIN")

    def on_cancel(self) -> None:
        self.parentApp.switchForm("MAIN")


class MainForm(npyscreen.FormBaseNewWithMenus):
    """..."""

    def create(self) -> None:
        """
        The create function is called when the form is created.
        It sets up the widgets and their initial values.
        """

        self.print_contacts_widget = self.add(npyscreen.TitlePager, name="Contacts:", begin_entry_at=1)

        self.menu = self.new_menu(name="Menu", shortcut="m")
        self.menu.addItem("Add contact", self.add_contact, "1")
        self.menu.addItem("Edit contact", self.edit_contact, "2")
        self.menu.addItem("Delete contact", self.delete_contact, "3")
        self.menu.addItem("Cloce Menu", self.close_menu, "^X")
        self.menu.addItem("Exit", self.exit, "^E")

    def beforeEditing(self) -> None:
        """
        The beforeEditing function is called before the form is displayed.
        It updates the list of contacts to be displayed in the form.
        """
        self.update_list()

    def update_list(self) -> None:
        """
        The update_list function updates the list of contacts in the address book to reflect any changes that have been made.
        """
        contacts = print_all_contacts(self.parentApp.addressbook)
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
                     lines=20, columns=130, draw_line=10)
        self.addForm('ADD CONTACT', AddContactForm, name='Add contact',
                     lines=20, columns=50, draw_line=1)
        self.addForm('EDIT CONTACT', EditContactForm, name='Edit contact',
                     lines=20, columns=50, draw_line=1)
        self.addForm('DELETE CONTACT', DeleteContactForm, name='Delete contact',
                     lines=10, columns=50, draw_line=1)


if __name__ == "__main__":
    AddressBookApp().run()
