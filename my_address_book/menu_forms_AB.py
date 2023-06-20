"""
The module provides the EditContactForm, DeleteContactForm, and AddContactForm classes for managing 
contacts in an address book application.

Classes:
    EditContactForm(npyscreen.ActionPopup):
        A form for editing a contact's information.

    DeleteContactForm(npyscreen.ActionPopup):
        A form for deleting a contact from the address book.
        
    AddContactForm(npyscreen.ActionForm):
        A form for adding a new contact to the address book.

"""


from datetime import datetime
import npyscreen

from my_address_book.utils import sanitize_phone_number
from my_address_book.validation import (
    name_validation,
    phone_validation,
    email_validation,
    birthday_date_validation,
    check_name_in_address_book,
    check_name_not_in_address_book,
)
from my_address_book.entities import Phone, User, Email
from my_address_book.records import RecordContact
from my_address_book.constants import FILE_AB


class EditContactForm(npyscreen.ActionPopup):
    """
    A form class for editing contact information.

    This form allows the user to edit a contact's name. It checks if the entered name exists in the address book,
    displays a message if it does, and prompts the user to enter another name. If the name is valid,
    the form switches to the ADD CONTACT form to edit the contact.

    Attributes:
        contact_name_for_change (npyscreen.TitleText): The widget for entering the contact name.

    """

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
            npyscreen.notify_confirm(message, "Error", editw=1)
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
            self.parentApp.getForm('ADD CONTACT').value = self.contact_name_for_change.value
            self.parentApp.getForm('ADD CONTACT').name = "Edit contact"
            self.parentApp.switchForm('ADD CONTACT')

    def on_cancel(self) -> None:
        """
        The on_cancel function is called when the user presses ^C or ^Q.
        It switches back to the MAIN form.
        """
        self.parentApp.switchForm("MAIN")


class DeleteContactForm(npyscreen.ActionPopup):
    """
    A form class for deleting a contact.

    This form allows the user to enter the name of a contact to delete. It checks if the entered name exists
    in the address book and prompts the user to confirm the deletion. If confirmed, the contact is deleted
    from the address book and saved to file.

    Attributes:
        contact_name_for_del (npyscreen.TitleText): The widget for entering the contact name to delete.

    """

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
            npyscreen.notify_confirm(message, "Error", editw=1)
            self.contact_name_for_del.value = None
            return False
        return True

    def delete_contact(self) -> str:
        """
        The delete_contact function is called when the user presses the 'Delete Contact' button.
        It deletes a contact from the address book, and saves it to file.
        """
        self.parentApp.addressbook.delete_record(self.contact_name_for_del.value)
        self.parentApp.addressbook.save_records_to_file(FILE_AB)
        return f"The contact '{self.contact_name_for_del.value}' has been deleted."

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
    """
    This class represents a form for adding or editing a contact in an address book.

    Attributes:
        value (str): 
            The value representing the contact to be edited (optional).
        contact_name (npyscreen.TitleText): 
            The widget for entering the contact's name.
        contact_phone_one (npyscreen.TitleText): 
            The widget for entering the first phone number.
        phone_assignment_one (npyscreen.TitleSelectOne): 
            The widget for selecting the assignment of the first phone number.
        contact_phone_two (npyscreen.TitleText): 
            The widget for entering the second phone number.
        phone_assignment_two (npyscreen.TitleSelectOne): 
            The widget for selecting the assignment of the second phone number.
        contact_phone_three (npyscreen.TitleText): 
            The widget for entering the third phone number.
        phone_assignment_three (npyscreen.TitleSelectOne): 
            The widget for selecting the assignment of the third phone number.
        contact_email_one (npyscreen.TitleText): 
            The widget for entering the first email address.
        email_assignment_one (npyscreen.TitleSelectOne): 
            The widget for selecting the assignment of the first email address.
        contact_email_two (npyscreen.TitleText): 
            The widget for entering the second email address.
        email_assignment_two (npyscreen.TitleSelectOne): 
            The widget for selecting the assignment of the second email address.
        contact_birth_text (npyscreen.TitleText): 
            The widget for entering the year of birth.
        contact_birth (npyscreen.TitleDateCombo): 
            The widget for selecting the date of birth.

    Methods:
        create(): Sets up the form and its widgets.
        beforeEditing(): Populates the form with data from the contact to be edited (if provided).
        after_editing(): Resets the form's values after editing is completed.
        data_validation(): Validates the data entered by the user.
        while_editing(*args, **kwargs): Converts the year of birth to a full date format while the user is editing.
        add_contact(): Creates a new contact object and adds it to the address book.
        change_contact(): Updates an existing contact with the modified information.
        on_ok(): Called when the user presses OK on the form, performs validation and adds or updates the contact.
        on_cancel(): Called when the user cancels the form, resets the form's values and returns to the main form.
    """

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
            record_contact: RecordContact = self.parentApp.addressbook.get_record(self.value)

            self.contact_name.value = record_contact.user.name

            if len(record_contact.phone_numbers) >= 1:
                self.contact_phone_one.value = (
                    record_contact.phone_numbers[0].subrecord.phone
                    if record_contact.phone_numbers[0].subrecord.phone
                    else None
                )
                self.phone_assignment_one.value = record_contact.phone_numbers[0].name

            if len(record_contact.phone_numbers) >= 2:
                self.contact_phone_two.value = (
                    record_contact.phone_numbers[1].subrecord.phone
                    if record_contact.phone_numbers[1].subrecord.phone
                    else None
                )
                self.phone_assignment_two.value = record_contact.phone_numbers[1].name

            if len(record_contact.phone_numbers) >= 3:
                self.contact_phone_three.value = (
                    record_contact.phone_numbers[2].subrecord.phone
                    if record_contact.phone_numbers[2].subrecord.phone
                    else None
                )
                self.phone_assignment_three.value = record_contact.phone_numbers[2].name

            if len(record_contact.emails) >= 1:
                self.contact_email_one.value = (
                    record_contact.emails[0].subrecord.email
                    if record_contact.emails[0].subrecord.email
                    else None
                )
                self.email_assignment_one.value = record_contact.emails[0].name

            if len(record_contact.emails) >= 2:
                self.contact_email_two.value = (
                    record_contact.emails[1].subrecord.email
                    if record_contact.emails[1].subrecord.email
                    else None
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
        message_error = name_validation(name)
        if message_error:
            npyscreen.notify_confirm(message_error, "Error", editw=1)
            self.contact_name.value = None
            return False

        if self.value != name:
            message_error = check_name_in_address_book(self.parentApp.addressbook, name)
            if message_error:
                npyscreen.notify_confirm(message_error, "Error", editw=1)
                self.contact_name.value = None
                return False

        if self.contact_phone_one.value:
            phone = sanitize_phone_number(self.contact_phone_one.value)
            message_error = phone_validation(phone)
            self.contact_phone_one.value = phone

        if message_error:
            npyscreen.notify_confirm(message_error, "Error", editw=1)
            self.contact_phone_one.value = None
            return False

        if self.contact_phone_two.value:
            phone = sanitize_phone_number(self.contact_phone_two.value)
            message_error = phone_validation(phone)
            self.contact_phone_two.value = phone

        if message_error:
            npyscreen.notify_confirm(message_error, "Error", editw=1)
            self.contact_phone_two.value = None
            return False

        if self.contact_phone_three.value:
            phone = sanitize_phone_number(self.contact_phone_three.value)
            message_error = phone_validation(phone)
            self.contact_phone_three.value = phone

        if message_error:
            npyscreen.notify_confirm(message_error, "Error", editw=1)
            self.contact_phone_three.value = None
            return False

        if self.contact_email_one.value:
            message_error = email_validation(self.contact_email_one.value)

        if message_error:
            npyscreen.notify_confirm(message_error, "Error", editw=1)
            self.contact_email_one.value = None
            return False

        if self.contact_email_two.value:
            message_error = email_validation(self.contact_email_two.value)

        if message_error:
            npyscreen.notify_confirm(message_error, "Error", editw=1)
            self.contact_email_two.value = None
            return False

        message_error = birthday_date_validation(self.contact_birth.value)
        if message_error:
            npyscreen.notify_confirm(message_error, "Error", editw=1)
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

        user = User(self.contact_name.value)
        contact = RecordContact(user)

        if self.contact_phone_one.value:
            phone_one = Phone(self.contact_phone_one.value)
            if self.phone_assignment_one.value:
                phone_assignment_one_value = [
                    self.phone_assignment_one.value[0],
                    self.phone_assignment_one.values[self.phone_assignment_one.value[0]]
                ]
                contact.add_phone_number(phone_one, phone_assignment_one_value)
            else:
                contact.add_phone_number(phone_one)

        if self.contact_phone_two.value:
            phone_two = Phone(self.contact_phone_two.value)
            if self.phone_assignment_two.value:
                phone_assignment_two_value = [
                    self.phone_assignment_two.value[0],
                    self.phone_assignment_two.values[self.phone_assignment_two.value[0]]
                ]
                contact.add_phone_number(phone_two, phone_assignment_two_value)
            else:
                contact.add_phone_number(phone_two)

        if self.contact_phone_three.value:
            phone_three = Phone(self.contact_phone_three.value)
            if self.phone_assignment_three.value:
                phone_assignment_three_value = [
                    self.phone_assignment_three.value[0],
                    self.phone_assignment_three.values[self.phone_assignment_three.value[0]]
                ]
                contact.add_phone_number(phone_three, phone_assignment_three_value)
            else:
                contact.add_phone_number(phone_three)

        if self.contact_email_one.value:
            email_one = Email(self.contact_email_one.value)
            if self.email_assignment_one.value:
                email_assignment_one = [
                    self.email_assignment_one.value[0],
                    self.email_assignment_one.values[self.email_assignment_one.value[0]]
                ]
                contact.add_email(email_one, email_assignment_one)
            else:
                contact.add_email(email_one)

        if self.contact_email_two.value:
            email_two = Email(self.contact_email_two.value)
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
        self.parentApp.addressbook.save_records_to_file(FILE_AB)
        return f"The contact '{self.contact_name.value}' has been added"

    def change_contact(self) -> str:
        """
        The function first deletes the selected contact, then calls add_contact() to create a new one 
        with updated information.
        """
        self.parentApp.addressbook.delete_record(self.value)
        message = self.add_contact()
        message = f"The contact '{self.contact_name.value}' has been updated"
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
