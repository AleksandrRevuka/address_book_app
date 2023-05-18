
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


class DeleteContactForm(npyscreen.ActionPopup):
    """..."""

    def create(self) -> None:
        """..."""
        self.contact_name_for_del = self.add(npyscreen.TitleText, name='Name')

    def check_name(self) -> bool:
        """..."""
        name = self.contact_name_for_del.value
        message = check_name_not_in_address_book(self.parentApp.addressbook, name)
        if message:
            npyscreen.notify_confirm(message)
            self.contact_name_for_del.value = None
            return False
        return True

    def delete_contact(self) -> str:
        """..."""
        self.parentApp.addressbook.delete_record(self.contact_name_for_del.value)
        self.parentApp.addressbook.save_records_to_file(FILE)
        return f"The contact '{self.contact_name_for_del.value.title()}' has been deleted."

    def on_ok(self) -> None:
        respon = self.check_name()
        if respon:
            message = self.delete_contact()
            npyscreen.notify_confirm(message, "Delete!", editw=1)

            self.parentApp.switchFormPrevious()

    def on_cancel(self) -> None:
        exiting = npyscreen.notify_yes_no(
            "Are you sure you want to cancel", editw=2)
        if exiting:
            npyscreen.notify_confirm(
                "OK. Contact has NOT been saved. Good bye", "Good bye!", editw=1)
            self.parentApp.setNextFormPrevious()
        else:
            npyscreen.notify_confirm(
                "You may continue working", "Okay", editw=1)


class AddContactForm(npyscreen.ActionForm):
    """..."""

    def create(self) -> None:
        """..."""
        self.contact_name = self.add(npyscreen.TitleText, name='Name')
        self.contact_phone = self.add(npyscreen.TitleText, name='Number phone')
        self.phone_assignment = self.add(npyscreen.TitleSelectOne,
                                         scroll_exit=True,
                                         max_height=4,
                                         name='Phone assignment',
                                         values=['Mobile',
                                                 'Home',
                                                 'Work'
                                                 ])
        self.contact_email = self.add(npyscreen.TitleText, name='Email')
        self.email_assignment = self.add(npyscreen.TitleSelectOne,
                                         scroll_exit=True,
                                         max_height=3,
                                         name='Email assignment',
                                         values=['Home',
                                                 'Work'
                                                 ])

        self.contact_birth_text = self.add(npyscreen.TitleText, name='Year Birth:')
        self.contact_birth = self.add(npyscreen.TitleDateCombo, name='Date Birth:', date_format='%d-%m-%Y',)
        self.contact_birth.when_parent_changes_value = self.while_editing

    def data_validation(self) -> bool:
        """..."""
        name = self.contact_name.value
        message = name_validation(name)
        if message:
            npyscreen.notify_confirm(message)
            self.contact_name.value = None
            return False

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
        """..."""
        if self.contact_birth_text.value:
            if self.contact_birth.value is None:
                birthday = datetime.strptime(str(int(self.contact_birth_text.value)), '%Y').date()
                self.contact_birth.value = birthday

    def add_contact(self) -> str:
        """..."""

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


    def on_ok(self) -> None:
        respon = self.data_validation()
        if respon:
            message = self.add_contact()
            npyscreen.notify_confirm(message, "Saved!", editw=1)

            self.parentApp.switchFormPrevious()

    def on_cancel(self) -> None:
        exiting = npyscreen.notify_yes_no(
            "Are you sure you want to cancel", editw=2)
        if exiting:
            npyscreen.notify_confirm(
                "OK. Contact has NOT been saved. Good bye", "Good bye!", editw=1)
            self.parentApp.setNextFormPrevious()
        else:
            npyscreen.notify_confirm(
                "You may continue working", "Okay", editw=1)


class MainForm(npyscreen.FormBaseNewWithMenus):
    """..."""

    def create(self) -> None:

        self.print_contacts_widget = self.add(npyscreen.TitlePager, name="Contacts:", begin_entry_at=1)

        self.menu = self.new_menu(name="Menu", shortcut="m")
        self.menu.addItem("Add contact", self.add_contact, "1")
        self.menu.addItem("Edit contact", self.edit_contact, "2")
        self.menu.addItem("Delete contact", self.delete_contact, "3")
        self.menu.addItem("Cloce Menu", self.close_menu, "^X")
        self.menu.addItem("Exit", self.exit, "^E")

    def beforeEditing(self) -> None:
        self.update_list()

    def update_list(self) -> None:
        contacts = print_all_contacts(self.parentApp.addressbook)
        self.print_contacts_widget.values = contacts.split('\n')
        self.print_contacts_widget.display()

    def add_contact(self) -> None:
        self.parentApp.switchForm("ADD CONTACT")

    def edit_contact(self) -> None:
        self.parentApp.switchForm("EDIT CONTACT")

    def delete_contact(self) -> None:
        self.parentApp.switchForm("DELETE CONTACT")

    def close_menu(self) -> None:
        self.parentApp.setNextFormPrevious()

    def exit(self) -> None:
        self.on_ok()

    def on_ok(self) -> None:
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
        npyscreen.setTheme(MyThemeWidgets)
        
        
        self.addressbook.read_records_from_file(FILE)

        self.addForm('MAIN', MainForm, name='Addressbook',
                     lines=20, columns=130, draw_line=10)
        self.addForm('ADD CONTACT', AddContactForm, name='Add contact',
                     lines=20, columns=50, draw_line=1)
        self.addForm('EDIT CONTACT', AddContactForm, name='Edit contact',
                     lines=20, columns=50, draw_line=1)
        self.addForm('DELETE CONTACT', DeleteContactForm, name='Delete contact',
                     lines=10, columns=50, draw_line=1)


if __name__ == "__main__":
    AddressBookApp().run()
