"""forms"""

from datetime import datetime
import npyscreen

from my_addressbook.utils import sanitize_phone_number
from my_addressbook.validation import (
    name_validation,
    phone_validation,
    email_validation,
    birthday_date_validation,
    check_name_in_address_book,
    check_name_not_in_address_book,
)
from my_addressbook.entities import Phone, User, Email
from my_addressbook.address_book import Record
from my_addressbook.constants import FILE


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
        if self.check_name():
            self.parentApp.getForm('ADD CONTACT').value = self.contact_name_for_change.value.lower()
            self.parentApp.getForm('ADD CONTACT').name = "Edit contact"
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
        self.parentApp.addressbook.delete_record(self.contact_name_for_del.value.lower())
        self.parentApp.addressbook.save_records_to_file(FILE)
        return f"The contact '{self.contact_name_for_del.value.title()}' has been deleted."

    def on_ok(self) -> None:
        """
        The on_ok function is called when the user presses enter on a form.
        It checks to see if the name entered by the user exists in our address book, and if it does, 
        it deletes that contact from our address book.
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
        self.contact_name: npyscreen.TitleText = self.add(npyscreen.TitleText, name='Name')
        self.contact_phone_one = self.add(npyscreen.TitleText, name='Number №1')
        self.phone_assignment_one = self.add(npyscreen.TitleSelectOne,
                                             scroll_exit=True,
                                             max_height=4,
                                             name='assignment',
                                             values=['home',
                                                     'mobile',
                                                     'work'
                                                     ])
        self.contact_phone_two = self.add_widget(npyscreen.TitleText, name='Number №2')
        self.phone_assignment_two = self.add(npyscreen.TitleSelectOne,
                                             scroll_exit=True,
                                             max_height=4,
                                             name='assignment',
                                             values=['home',
                                                     'mobile',
                                                     'work'
                                                     ])
        self.contact_phone_three = self.add_widget(npyscreen.TitleText, name='Number №3')
        self.phone_assignment_three = self.add(npyscreen.TitleSelectOne,
                                               scroll_exit=True,
                                               max_height=4,
                                               name='assignment',
                                               values=['home',
                                                       'mobile',
                                                       'work'
                                                       ])

        self.contact_email_one = self.add(npyscreen.TitleText, name='Email №1')
        self.email_assignment_one = self.add(npyscreen.TitleSelectOne,
                                             scroll_exit=True,
                                             max_height=3,
                                             name='Email assignment',
                                             values=['home',
                                                     'work'
                                                     ])

        self.contact_email_two = self.add(npyscreen.TitleText, name='Email №2')
        self.email_assignment_two = self.add(npyscreen.TitleSelectOne,
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
            record_contact: Record = self.parentApp.addressbook.get_contact(self.value)

            self.contact_name.value = record_contact.user.name
            self.contact_phone_one.value = (
                record_contact.phone_numbers[0].subrecord.phone
                if record_contact.phone_numbers[0].subrecord.phone
                else ''
            )
            self.phone_assignment_one.value = record_contact.phone_numbers[0].name

            if len(record_contact.phone_numbers) >= 2:
                self.contact_phone_two.value = (
                    record_contact.phone_numbers[1].subrecord.phone
                    if record_contact.phone_numbers[1].subrecord.phone
                    else ''
                )
                self.phone_assignment_two.value = record_contact.phone_numbers[1].name

            if len(record_contact.phone_numbers) >= 3:
                self.contact_phone_three.value = (
                    record_contact.phone_numbers[2].subrecord.phone
                    if record_contact.phone_numbers[2].subrecord.phone
                    else ''
                )
                self.phone_assignment_three.value = record_contact.phone_numbers[2].name

            self.contact_email_one.value = (
                record_contact.emails[0].subrecord.email
                if record_contact.emails[0].subrecord.email
                else ''
            )
            self.email_assignment_one.value = record_contact.emails[0].name
            self.contact_birth.value = record_contact.user.birthday_date

            if len(record_contact.emails) >= 2:
                self.contact_email_two.value = (
                    record_contact.emails[1].subrecord.email
                    if record_contact.emails[1].subrecord.email
                    else ''
                )
                self.email_assignment_two.value = record_contact.emails[1].name

            self.contact_birth.value = record_contact.user.birthday_date

    def after_editing(self) -> None:
        """
        The afterEditing function is called after the user has finished editing a form.
        It allows you to perform any actions that are required, such as updating the database with new values.
        The function takes one argument: self, which is a reference to the form itself.
        """
        self.value = None
        self.contact_name.value = None

        self.contact_phone_one.value = None
        self.phone_assignment_one.value = None
        self.contact_phone_two.value = None
        self.phone_assignment_two.value = None
        self.contact_phone_three.value = None
        self.phone_assignment_three.value = None

        self.contact_email_one.value = None
        self.email_assignment_one.value = None
        self.contact_email_two.value = None
        self.email_assignment_two.value = None

        self.contact_birth_text.value = None
        self.contact_birth.value = None

        self.parentApp.getForm('ADD CONTACT').name = "Add contact"

    def data_validation(self) -> bool:
        """
        The data_validation function checks the validity of the data entered by
        the user. It returns True if all data is valid, and False otherwise.
        """

        name = self.contact_name.value
        message = name_validation(name)
        if message:
            npyscreen.notify_confirm(message)
            self.contact_name.value = None
            return False

        if self.value != name.lower():
            message = check_name_in_address_book(self.parentApp.addressbook, name)
            if message:
                npyscreen.notify_confirm(message)
                self.contact_name.value = None
                return False

        if self.contact_phone_one.value:
            phone = self.contact_phone_one.value
            phone = sanitize_phone_number(phone)
            message = phone_validation(phone)
            self.contact_phone_one.value = phone

        if message:
            npyscreen.notify_confirm(message)
            self.contact_phone_one.value = None
            return False

        if self.contact_phone_two.value:
            phone = self.contact_phone_two.value
            phone = sanitize_phone_number(phone)
            message = phone_validation(phone)
            self.contact_phone_two.value = phone

        if message:
            npyscreen.notify_confirm(message)
            self.contact_phone_two.value = None
            return False

        if self.contact_phone_three.value:
            phone = self.contact_phone_three.value
            phone = sanitize_phone_number(phone)
            message = phone_validation(phone)
            self.contact_phone_three.value = phone

        if message:
            npyscreen.notify_confirm(message)
            self.contact_phone_three.value = None
            return False

        if self.contact_email_one.value:
            email = self.contact_email_one.value
            message = email_validation(email)
        if message:
            npyscreen.notify_confirm(message)
            self.contact_email_one.value = None
            return False

        if self.contact_email_two.value:
            email = self.contact_email_two.value
            message = email_validation(email)
        if message:
            npyscreen.notify_confirm(message)
            self.contact_email_two.value = None
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
            if not self.contact_birth.value:
                birthday = datetime.strptime(str(int(self.contact_birth_text.value)), '%Y').date()
                self.contact_birth.value = birthday

    def add_contact(self) -> str:
        """
        The add_contact function takes the user input from the AddContactForm and
        creates a new contact object. It then adds that contact to the address book,
        and saves it to file.
        """

        email_one = Email(self.contact_email_one.value)
        email_two = Email(self.contact_email_two.value)
        phone_one = Phone(self.contact_phone_one.value)
        phone_two = Phone(self.contact_phone_two.value)
        phone_three = Phone(self.contact_phone_three.value)

        user = User(self.contact_name.value)
        contact = Record(user)
        if self.phone_assignment_one.value:
            phone_assignment_one_value = [
                self.phone_assignment_one.value[0],
                self.phone_assignment_one.values[self.phone_assignment_one.value[0]]
            ]
            contact.add_phone_number(phone_one, phone_assignment_one_value)
        else:
            contact.add_phone_number(phone_one)

        if self.phone_assignment_two.value:
            phone_assignment_two_value = [
                self.phone_assignment_two.value[0],
                self.phone_assignment_two.values[self.phone_assignment_two.value[0]]
            ]
            contact.add_phone_number(phone_two, phone_assignment_two_value)
        else:
            contact.add_phone_number(phone_two)

        if self.phone_assignment_three.value:
            phone_assignment_three_value = [
                self.phone_assignment_three.value[0],
                self.phone_assignment_three.values[self.phone_assignment_three.value[0]]
            ]
            contact.add_phone_number(phone_three, phone_assignment_three_value)
        else:
            contact.add_phone_number(phone_three)

        if self.email_assignment_one.value:
            email_assignment_one = [
                self.email_assignment_one.value[0],
                self.email_assignment_one.values[self.email_assignment_one.value[0]]
            ]
            contact.add_email(email_one, email_assignment_one)
        else:
            contact.add_email(email_one)

        if self.email_assignment_two.value:
            email_assignment_two = [
                self.email_assignment_two.value[0],
                self.email_assignment_two.values[self.email_assignment_two.value[0]]
            ]
            contact.add_email(email_two, email_assignment_two)
        else:
            contact.add_email(email_two)

        contact.add_birthday(self.contact_birth.value)

        self.parentApp.addressbook.add_record(contact)
        self.parentApp.addressbook.save_records_to_file(FILE)
        return f"The contact '{self.contact_name.value.title()}' has been added"

    def change_contact(self) -> str:
        """
        The function first deletes the selected contact, then calls add_contact() to create a new one 
        with updated information.
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
        if self.data_validation():
            if not self.value:
                message = self.add_contact()
                self.after_editing()
                npyscreen.notify_confirm(message, "Saved!", editw=1)

            else:
                message = self.change_contact()
                self.after_editing()
                npyscreen.notify_confirm(message, "Saved!", editw=1)

            self.parentApp.switchForm("MAIN")

    def on_cancel(self) -> None:
        self.after_editing()
        self.parentApp.switchForm("MAIN")