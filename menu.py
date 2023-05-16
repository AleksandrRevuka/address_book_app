
from datetime import datetime
import npyscreen
from prettytable import PrettyTable

from utils import sanitize_phone_number
from validation import (
    verify_name,
    verify_phone,
    verify_email,
    verify_birthday_date,
    verify_criteria,
    check_name_in_address_book,
    check_name_not_in_address_book,
    check_phone_number_in_address_book,
    check_phone_number_not_in_address_book,
    check_email_in_address_book,
    check_email_not_in_address_book,
)
from constants import (NUMBER_OF_CONTACTS_PER_PAGE, FILE, HELP)
from address_book import Record, AddressBook as AB
from entities import Phone, User, Email

class AddContactForm(npyscreen.ActionForm):
    """..."""
    def create(self) -> None:
        """..."""
        self.contact_name = self.add(npyscreen.TitleText, name='Name')
        self.contact_name.when_cursor_moved = self.validate_name
        self.contact_phone = self.add(npyscreen.TitleText, name='Number phone')
        
        self.frame_birth_text = self.add(npyscreen.TitleText, name='Year Birth:')
        self.frame_birth = self.add(npyscreen.TitleDateCombo, name='Date Birth:', date_format='%d-%m-%Y',)
        self.frame_birth.when_cursor_moved = self.while_editing
        
        # self.myDepartment = self.add(npyscreen.TitleSelectOne,
        #                              scroll_exit=True,
        #                              max_height=3,
        #                              name='Department',
        #                              values=['Department 1',
        #                                      'Department 2',
        #                                      'Department 3'
        #                                      ])
    
    def validate_name(self) -> None:
        """..."""
        name = self.contact_name.value
        message = verify_name(name)
        if message:
            npyscreen.notify_confirm(message)
    
    def while_editing(self, *args: list, **kwargs: dict) -> None:
        """..."""
        if self.frame_birth_text.value:
            birthday = datetime.strptime(str(int(self.frame_birth_text.value)), '%Y').date()
            self.frame_birth.value = birthday
     
    def add_contact(self, contact_name: str,
                    phone_number: str, 
                    contact_email: str, 
                    birthday_date: str,
                    phone_assignment:str,
                    email_assignment: str) -> None:
        """..."""
        check_name_in_address_book(self.parentApp.addressbook, contact_name)
        verify_name(contact_name)
        phone_number = sanitize_phone_number(phone_number)
        verify_phone(phone_number)
        verify_email(contact_email)
        verify_birthday_date(birthday_date)
        
        email = Email(contact_email)
        phone = Phone(phone_number)
        user = User(contact_name)
        contact = Record(user)
        contact.add_phone_number(phone, phone_assignment)
        contact.add_email(email, email_assignment)
        contact.add_birthday(birthday_date)
        
        self.parentApp.addressbook.add_record(contact)
        self.parentApp.addressbook.save_records_to_file(FILE)
        print(f"The contact '{contact_name.title()}' has been added: {phone.phone}")
        
     
    def on_ok(self) -> None:

        npyscreen.notify_confirm("Form has been saved", "Saved!", editw=1)
        self.parentApp.switchFormPrevious()

    def on_cancel(self) -> None:
        exiting = npyscreen.notify_yes_no(
            "Are you sure you want to cancel", editw=2)
        if exiting:
            npyscreen.notify_confirm(
                "OK. From has NOT been saved. Good bye", "Good bye!", editw=1)
            self.parentApp.setNextFormPrevious()
        else:
            npyscreen.notify_confirm(
                "You may continue working", "Okay", editw=1)


class MainForm(npyscreen.ActionFormWithMenus, npyscreen.SplitForm):
    """..."""
    def create(self):
        
        self.menu = self.new_menu(name="Main Menu", shortcut="m")
        self.menu.addItem("Add contact", self.add_contact, "1")
        self.menu.addItem("Print contact", self.print_contact, "2")
        self.menu.addItem("Delete contact", self.delete_contact, "3")
        self.menu.addItem("Exit Menu", self.exit_menu, "^X")

    def add_contact(self):
        self.parentApp.switchForm("ADD CONTACT")

    def print_contact(self):
        self.parentApp.switchForm("PRINT CONTACT")
        
    def delete_contact(self):
        self.parentApp.switchForm("DELETE CONTACT")
        # npyscreen.notify_confirm("You press Item_2!", "Item_2", editw=1)

    def exit_menu(self):
        self.parentApp.setNextFormPrevious()

    def on_ok(self):
        npyscreen.notify_confirm("Form has been saved", "Saved!", editw=1)
        self.parentApp.setNextForm(None)

    def on_cancel(self):
        exiting = npyscreen.notify_yes_no(
            "Are you sure you want to cancel", editw=2)
        if exiting:
            npyscreen.notify_confirm(
                "OK. From has NOT been saved. Good bye", "Good bye!", editw=1)
            self.parentApp.setNextForm(None)
        else:
            npyscreen.notify_confirm(
                "You may continue working", "Okay", editw=1)



class AddressBookApp(npyscreen.NPSAppManaged):
    """..."""

    def onStart(self):
        self.addressbook = AB()
        self.addressbook.read_records_from_file(FILE)
        
        self.addForm('MAIN', MainForm, name='main menu',
                     lines=20, columns=150, draw_line=10)
        self.addForm('ADD CONTACT', AddContactForm, name='add contact',
                     lines=20, columns=75, draw_line=1)
        self.addForm('PRINT CONTACT', AddContactForm, name='print contact',
                     lines=20, columns=75, draw_line=1)
        self.addForm('DELETE CONTACT', AddContactForm, name='delete contact',
                     lines=20, columns=75, draw_line=1)


if __name__ == "__main__":
    app = AddressBookApp().run()