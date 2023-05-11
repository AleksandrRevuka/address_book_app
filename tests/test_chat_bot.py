"""Tests commands"""

import unittest
from unittest.mock import patch
import io

from address_book import Record, AddressBook
from entities import Phone, User, Email
from run_bot import (
    add_contact,
    # print_contact,
    # delete_contact,
    # add_phone_number_to_contact,
    # change_phone_number_contact,
    # delete_phone_number_contact,
    # add_email_to_contact,
    # change_email_contact,
    # delete_email_contact,
    # add_birthday_to_contact,
    # change_birthday_contact,
    # serch_contact,
    # print_contacts,
)


class TestChatBot(unittest.TestCase):
    """Tests commands"""

    def setUp(self) -> None:
        self.addressbook_test = AddressBook()
        self.user_test = User('sasha')
        self.phone_test = Phone('380951234567')
        self.email_test = Email('test_sasha@gmail.com')
        self.record_test = Record(self.user_test)
        self.record_test.add_phone_number(self.phone_test)
        self.record_test.add_email(self.email_test)
        self.user_name = 'Bob'

    def tearDown(self) -> None:
        del self.addressbook_test
        del self.record_test
        del self.user_test
        del self.phone_test
        del self.email_test

    def test_add_contact__with_valid_input(self):
        """
        The test_add_contact_exists function tests the add_contact function.
        It checks that if a contact with the same name already exists in an address book, 
        the user will be notified about it.
        """
        name_test = 'sasha'
        phone_test = '380951234567'
        self.addressbook_test.add_record(self.record_test)

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            
            add_contact(self.addressbook_test,
                    name_test,
                    phone_test)
            
        self.assertTrue(f"The contact '{name_test.title()}' has been" in fake_out.getvalue())

    # def test_add_contact_without_name(self):
    #     """
    #     The test_add_contact_without_name function tests the add_contact function.
    #     The test checks that the function returns a message about an error in entering data, 
    #     if you try to add a contact without specifying its name.
    #     """
    #     name_test = None
    #     phone_test = '380951234567'

    #     message = add_contact(self.addressbook_test,
    #                           name_test,
    #                           phone_test)
    #     self.assertTrue('After the command, you must enter the new' in message)

    # def test_add_contact_without_phone(self):
    #     """
    #     The test_add_contact_without_phone function tests the add_contact function in AddressBook.py
    #         to ensure that it returns a message prompting the user to enter a phone number if they do not 
    #         provide one when adding a new contact.
    #     """
    #     name_test = 'Sasha'
    #     phone_test = None

    #     message = add_contact(self.addressbook_test,
    #                           name_test,
    #                           phone_test)
    #     self.assertTrue('After the command, you must enter the new' in message)

    # def test_change_phone_number_contact_not_exists_name(self):
    #     """
    #     The function tests the change_number_contact function.
    #     The test is performed on an addressbook that contains a user with name 'user' and no contacts.
    #     The test checks if the change_number_contact function returns a message containing 'was not found'. 
    #     This means that the contact was not found in the addressbook.
    #     """
    #     contact_name = 'Sasha'
    #     new_phone_number = '380951234567'
    #     old_phone_number = '380951234500'

    #     message = change_phone_number_contact(self.addressbook_test,
    #                                     contact_name,
    #                                     new_phone_number,
    #                                     old_phone_number)
    #     self.assertTrue('was not found' in message)

    # def test_change_phone_number_contact_not_exists_number(self):
    #     """
    #     The function tests the change_number_contact function.
    #     The test checks that the change_number_contact function returns a message indicating that 
    #     the contact was not found in the address book when trying to change a phone number of a contact 
    #     that does not exist in an address book.
    #     """
    #     contact_name = 'Sasha'
    #     new_phone_number = '380951234567'
    #     old_phone_number = '380951234500'

    #     self.addressbook_test.add_record(self.record_test)

    #     message = change_phone_number_contact(self.addressbook_test,
    #                                     contact_name,
    #                                     new_phone_number,
    #                                     old_phone_number)
    #     self.assertTrue('was not found in the address book' in message)

    # def test_change_phone_number_contact_number_exists_in_contact(self):
    #     """
    #     The function tests the change_number_contact function.
    #     The test checks that if a user tries to change a contact's phone number to one that already exists in this contact, 
    #     the system will return an error message.
    #     """
    #     contact_name = 'Sasha'
    #     new_phone_number = '380951234567'
    #     old_phone_number = '380951234500'

    #     self.addressbook_test.add_record(self.record_test)
    #     self.record_test.add_phone_number(Phone(old_phone_number))

    #     message = change_phone_number_contact(self.addressbook_test,
    #                                     contact_name,
    #                                     new_phone_number,
    #                                     old_phone_number)
    #     self.assertTrue('already exists in this' in message)

    # def test_change_phone_number_contact_without_name(self):
    #     """
    #     The function tests the change_number_contact function.
    #     The test checks that the function returns a message about entering a contact name after executing 
    #     the command if there is no contact name in the arguments of this function.
    #     """
    #     contact_name = None
    #     new_phone_number = '380951234567'
    #     old_phone_number = '380951234500'

    #     message = change_phone_number_contact(self.addressbook_test,
    #                                     contact_name,
    #                                     new_phone_number,
    #                                     old_phone_number)
    #     self.assertTrue('After the command, you must enter' in message)

    # def test_change_phone_number_contact_without_new_phone(self):
    #     """
    #     The function tests the change_number_contact function.
    #     The test checks that the user is prompted to enter a new phone number if he/she does not provide one.
    #     """
    #     contact_name = 'Sasha'
    #     new_phone_number = None
    #     old_phone_number = '380951234500'

    #     message = change_phone_number_contact(self.addressbook_test,
    #                                     contact_name,
    #                                     new_phone_number,
    #                                     old_phone_number)
    #     self.assertTrue('After the command, you must enter' in message)

    # def test_change_phone_number_contact_without_old_phone(self):
    #     """
    #     The function tests the change_number_contact function.
    #     The test checks that the user is prompted to enter an old phone number if he/she does not provide one.
    #     """
    #     contact_name = 'Sasha'
    #     new_phone_number = '380951234567'
    #     old_phone_number = None

    #     message = change_phone_number_contact(self.addressbook_test,
    #                                     contact_name,
    #                                     new_phone_number,
    #                                     old_phone_number)
    #     self.assertTrue('After the command, you must enter' in message)

    # def test_print_contact_not_exists_name(self):
    #     """
    #     The function tests the print_contact function in AddressBook.py
    #         to ensure that it returns a message indicating that the contact was not found if no contact with 
    #         the given name exists in the address book.
    #     """
    #     contact_name = 'Sasha'

    #     message = print_contact(self.addressbook_test,
    #                             contact_name)

    #     self.assertTrue('was not found' in message)

    # def test_print_contact_without_name(self):
    #     """
    #     The function tests the print_contact function in AddressBook.py
    #         to ensure that it returns an error message when a user attempts to print a contact without entering 
    #         the name of the contact they wish to print.
    #     """
    #     contact_name = None

    #     message = print_contact(self.addressbook_test,
    #                             contact_name)

    #     self.assertTrue('After the command, you must enter' in message)

    # def test_delete_contact_not_exists_name(self):
    #     """
    #     The function tests the delete_contact function in AddressBook.py
    #         to ensure that it returns a message indicating that the contact was not found if a user attempts to 
    #         delete a contact from their address book who does not exist.
    #     """
    #     contact_name = 'Sasha'

    #     message = delete_contact(self.addressbook_test,
    #                              contact_name)
    #     self.assertTrue('was not found' in message)

    # def test_delete_contact_without_name(self):
    #     """
    #     The function tests the delete_contact function in the AddressBook module.
    #     The function creates an addressbook object, a record object, and a user name. 
    #     It then adds the record to the addressbook using add_record from AddressBook. It then calls delete contact with 
    #     the address book, user name and no contact name (None). The assertTrue statement checks that if you call delete 
    #     with no contact name it will return 'After command you must enter' which is what we want.
    #     """
    #     contact_name = None

    #     self.addressbook_test.add_record(self.record_test)

    #     message = delete_contact(self.addressbook_test,
    #                              contact_name)
    #     self.assertTrue('After the command, you must enter' in message)

    # def test_delete_phone_number_contact_not_exists_name(self):
    #     """
    #     The function tests the delete_contact_phone function.
    #     It checks that if a contact with the given name does not exist, then an appropriate message is returned.
    #     """
    #     contact_name = 'Sasha'
    #     phone_number = '380951234567'

    #     message = delete_phone_number_contact(self.addressbook_test,
    #                                         contact_name,
    #                                         phone_number)
    #     self.assertTrue('was not found' in message)

    # def test_delete_phone_number_contact_not_exists_number(self):
    #     """
    #     The function tests the delete_contact_phone function.
    #     The test is successful if the message returned by the function contains 'was not found in the'
    #     """
    #     contact_name = 'Sasha'
    #     phone_number = '380951234500'

    #     self.addressbook_test.add_record(self.record_test)

    #     message = delete_phone_number_contact(self.addressbook_test,
    #                                         contact_name,
    #                                         phone_number)
    #     self.assertTrue('was not found in the' in message)

    # def test_delete_phone_number_contact_without_name(self):
    #     """
    #     The function tests the delete_contact_phone function.
    #     The test checks that the function returns a message about entering a contact name after 
    #     the command if no contact name is entered.
    #     """
    #     contact_name = None
    #     phone_number = '380951234567'

    #     message = delete_phone_number_contact(self.addressbook_test,
    #                                         contact_name,
    #                                         phone_number)
    #     self.assertTrue('After the command, you must enter' in message)

    # def test_delete_phone_number_contact_without_phone(self):
    #     """
    #     The function tests the delete_contact_phone function in AddressBook.py
    #         to ensure that it returns a message stating that the user must enter a phone number after entering the command 
    #         if no phone number is entered after entering the command.
    #     """
    #     contact_name = 'Sasha'
    #     phone_number = None

    #     message = delete_phone_number_contact(self.addressbook_test,
    #                                    contact_name,
    #                                    phone_number)
    #     self.assertTrue('After the command, you must enter' in message)

    # def test_add_phone_number_to_contact_not_exists_name(self):
    #     """
    #     The function tests the add_number_phone_to_contact function.
    #     It checks that if a contact with the given name does not exist, then an error message is returned.
    #     """
    #     contact_name = 'Sasha'
    #     phone_number = '380951234567'

    #     message = add_phone_number_to_contact(self.addressbook_test,
    #                                           contact_name,
    #                                           phone_number)
    #     self.assertTrue('was not found' in message)

    # def test_add_phone_number_to_contact_exists_number(self):
    #     """
    #     The function tests the add_number_phone_to_contact function.
    #     The test checks that the message returned by the function is correct when a user tries to add an existing phone number to a contact.
    #     """
    #     contact_name = 'Sasha'
    #     phone_number = '380951234567'

    #     self.addressbook_test.add_record(self.record_test)
    #     self.record_test.add_phone_number(Phone(phone_number))

    #     message = add_phone_number_to_contact(self.addressbook_test,
    #                                           contact_name,
    #                                           phone_number)
    #     self.assertTrue('already exists in the' in message)

    # def test_add_number_phone_to_contact_without_name(self):
    #     """
    #     The function tests the add_number_phone_to_contact function.
    #     The test checks that the function returns a message about entering a contact name after entering the command.
    #     """
    #     contact_name = None
    #     phone_number = '380951234567'

    #     message = add_phone_number_to_contact(self.addressbook_test,
    #                                           contact_name,
    #                                           phone_number)
    #     self.assertTrue('After the command, you must enter' in message)

    # def test_add_number_phone_to_contact_without_phone(self):
    #     """
    #     The function tests the add_number_phone_to_contact function.
    #     The test is performed by calling the add_number_phone method with a contact name and no phone number.
    #     The expected result is that an error message will be returned, indicating that a phone number must be entered.
    #     """
    #     contact_name = 'Sasha'
    #     phone_number = None

    #     message = add_phone_number_to_contact(self.addressbook_test,
    #                                           contact_name,
    #                                           phone_number)
    #     self.assertTrue('After the command, you must enter' in message)

    # def test_add_birthday_date_not_exists_name(self):
    #     """
    #     The test_add_birthday_date_not_exists_name function tests the add_birthday_date function in AddressBook.py
    #         to ensure that it returns a message stating that the contact was not found if a user attempts to add 
    #         a birthday date for someone who is not in their address book.
    #     """
    #     contact_name = 'Sasha'
    #     birthday_date = '26-06-1982'

    #     message = add_birthday_to_contact(self.addressbook_test,
    #                                 contact_name,
    #                                 birthday_date)
    #     self.assertTrue('was not found' in message)

    # def test_add_birthday_to_contact_without_name(self):
    #     """
    #     The function tests the add_birthday_date function.
    #     It checks that if a user tries to add a birthday date without entering the name of the contact, 
    #     the program will return an error message.
    #     """
    #     contact_name = None
    #     birthday_date = '26-06-1982'

    #     message = add_birthday_to_contact(self.addressbook_test,
    #                                 contact_name,
    #                                 birthday_date)
    #     self.assertTrue('After the command, you must enter' in message)

    # def test_add_birthday_to_contact_without_birthday(self):
    #     """
    #     The function tests the add_birthday_date function.
    #     The test is successful if the message returned by add_birthday_date contains 'After the command, you must enter'.
    #     """
    #     contact_name = 'Sasha'
    #     birthday_date = None

    #     message = add_birthday_to_contact(self.addressbook_test,
    #                                 contact_name,
    #                                 birthday_date)
    #     self.assertTrue('After the command, you must enter' in message)

    # def test_change_birthday_contacte_not_exists_name(self):
    #     """
    #     The function tests the change_birthday_date function in AddressBook.py
    #         to ensure that it returns a message stating that the contact was not found if a user attempts to change 
    #         the birthday date of a contact who does not exist in their address book.
    #     """
    #     contact_name = 'Sasha'
    #     birthday_date = '26-06-1982'

    #     message = change_birthday_contact(self.addressbook_test,
    #                                    contact_name,
    #                                    birthday_date)
    #     self.assertTrue('was not found' in message)

    # def test_change_birthday_contact_without_name(self):
    #     """
    #     The function tests the change_birthday_date function in AddressBook.py
    #         to ensure that it returns an error message when a user attempts to change the birthday date of a contact without 
    #         specifying which contact's birthday date they want to change.
    #     """
    #     contact_name = None
    #     birthday_date = '26-06-1982'

    #     message = change_birthday_contact(self.addressbook_test,
    #                                    contact_name,
    #                                    birthday_date)
    #     self.assertTrue('After the command, you must enter' in message)

    # def test_change_birthday_contact_without_birthday(self):
    #     """
    #     The function tests the change_birthday_date function in AddressBook.py
    #         to see if it returns a message that tells the user to enter a birthday date after entering the command.
    #     """
    #     contact_name = 'Sasha'
    #     birthday_date = None

    #     message = change_birthday_contact(self.addressbook_test,
    #                                    contact_name,
    #                                    birthday_date)
    #     self.assertTrue('After the command, you must enter' in message)

    # def test_serch_contact_criteria_not_isdigit_isalpha(self):
    #     """
    #     The test_serch_contact_criteria_not_isdigit_isalpha function tests the serch_contact function in AddressBook.py
    #         to ensure that it returns an error message when a user enters a search criteria that is not all numbers or letters.
    #     """
    #     criteria = '/.,mnb'

    #     message = serch_contact(self.addressbook_test,
    #                             criteria)
    #     self.assertTrue('must be only numbers or letters' in message)

    # def test_serch_contact_criteria_without_criteria(self):
    #     """
    #     The test_serch_contact_criteria_without_criteria function tests the serch_contact function in AddressBook.py
    #         to ensure that it returns a message stating that the user must enter criteria if they do not provide any.
    #     """
    #     criteria = None

    #     message = serch_contact(self.addressbook_test,
    #                             criteria)
    #     self.assertTrue(
    #         'After command, you must enter the criteria of serch' in message)

    # def test_add_email_to_contact_not_exists_name(self):
    #     """
    #     The test_add_email_to_contact_not_exists_name function tests the add_email_to_contact function in AddressBook.py
    #         to ensure that it returns a message stating that the contact was not found if a user attempts to add an email
    #         address to a contact who does not exist in their address book.
    #     """
    #     contact_name = 'Sasha'
    #     email = 'test_sasha@gmail.com'

    #     message = add_email_to_contact(self.addressbook_test,
    #                                           contact_name,
    #                                           email)
    #     self.assertTrue('was not found' in message)

    # def test_add_email_to_contact_exists_email(self):
    #     """
    #     The test_add_email_to_contact_exists_email function tests the add_email_to_contact function in the AddressBook module.
    #     The test is successful if an error message is returned when a user attempts to add an email address that already exists for a contact.
    #     """
    #     contact_name = 'Sasha'
    #     email = 'test_sasha@gmail.com'

    #     self.addressbook_test.add_record(self.record_test)
    #     self.record_test.add_email(Email(email))

    #     message = add_email_to_contact(self.addressbook_test,
    #                                           contact_name,
    #                                           email)
    #     self.assertTrue('already exists in this' in message)

    # def test_add_email_to_contact_without_name(self):
    #     """
    #     The test_add_email_to_contact_without_name function tests the add_email_to_contact function.
    #     The test is performed by calling the add_email_to_contact function with a contact name of None, and an email address of 'test@gmail.com'.
    #     The expected result is that the message returned from this call should contain 'After the command, you must enter'
    #     """
    #     contact_name = None
    #     email = 'test_sasha@gmail.com'

    #     message = add_email_to_contact(self.addressbook_test,
    #                                           contact_name,
    #                                           email)
    #     self.assertTrue('After the command, you must enter' in message)

    # def test_add_email_to_contact_without_email(self):
    #     """
    #     The test_add_email_to_contact_without_email function tests the add_email_to_contact function.
    #     The test is successful if the message returned by add_email_to contact contains 'After the command, you must enter'
    #     """
    #     contact_name = 'Sasha'
    #     email = None

    #     message = add_email_to_contact(self.addressbook_test,
    #                                           contact_name,
    #                                           email)
    #     self.assertTrue('After the command, you must enter' in message)

    # def test_change_email_contact_not_exists_name(self):
    #     """
    #     The test_change_email_contact_not_exists_name function tests the change_email_contact function in AddressBook.py
    #         to ensure that it returns a message stating that the contact was not found if the user attempts to change an email
    #         address for a contact who does not exist in their address book.
    #     """
    #     contact_name = 'Sasha'
    #     new_email = 'test_sasha_new@gmail.com'
    #     old_email = 'test_sasha@gmail.com'

    #     message = change_email_contact(self.addressbook_test,
    #                                     contact_name,
    #                                     new_email,
    #                                     old_email)
    #     self.assertTrue('was not found' in message)

    # def test_change_email_contact_not_exists_email(self):
    #     """
    #     The test_change_email_contact_not_exists_email function tests the change_email_contact function in the AddressBook module.
    #     The test is designed to check if a contact with an email that does not exist in the address book can be changed.
    #     The test creates an instance of Record, AddressBook, Phone, User and Email classes and assigns them to variables record_test, 
    #     addressbook_test, phone_test user name and email respectively. The add method from the Record class is used to add a new record 
    #     into our address book using our previously created instances of Phone and Email classes as parameters for this method call. 
    #     The change_email function from AddressBook class is then called

    #     """
    #     contact_name = 'Sasha'
    #     new_email = 'test_sasha_new@gmail.com'
    #     old_email = 'test_sasha_old@gmail.com'

    #     self.addressbook_test.add_record(self.record_test)

    #     message = change_email_contact(self.addressbook_test,
    #                                     contact_name,
    #                                     new_email,
    #                                     old_email)
    #     self.assertTrue('was not found in the' in message)

    # def test_change_email_contact_email_exists_in_contact(self):
    #     """
    #     The test_change_email_contact_email_exists_in_contact function tests the change_email_contact function in the AddressBook module.
    #     The test is successful if a message is returned that states that the email already exists in this contact.
    #     """
    #     contact_name = 'Sasha'
    #     new_email = 'test_sasha.new@gmail.com'
    #     old_email = 'test_sasha@gmail.com'

    #     self.addressbook_test.add_record(self.record_test)
    #     self.record_test.add_email(Email(new_email))

    #     message = change_email_contact(self.addressbook_test,
    #                                     contact_name,
    #                                     new_email,
    #                                     old_email)
    #     self.assertTrue('already exists in this' in message)

    # def test_change_email_contact_without_name(self):
    #     """
    #     The test_change_email_contact_without_name function tests the change_email_contact function in AddressBook.py
    #         to see if it returns an error message when a user tries to change the email of a contact without entering
    #         their name first.
    #     """
    #     contact_name = None
    #     new_email = 'test_sasha_new@gmail.com'
    #     old_email = self.email_test

    #     message = change_email_contact(self.addressbook_test,
    #                                     contact_name,
    #                                     new_email,
    #                                     old_email)
    #     self.assertTrue('After the command, you must enter' in message)

    # def test_change_email_contact_without_new_email(self):
    #     """
    #     The test_change_email_contact_without_new_email function tests the change_email_contact function in AddressBook.py
    #         to ensure that it returns a message prompting the user for an email address if no new email is provided.
    #     """
    #     contact_name = 'Sasha'
    #     new_email = None
    #     old_email = self.email_test

    #     message = change_email_contact(self.addressbook_test,
    #                                     contact_name,
    #                                     new_email,
    #                                     old_email)
    #     self.assertTrue('After the command, you must enter' in message)

    # def test_change_email_contact_without_old_email(self):     
    #     """
    #     The test_change_email_contact_without_old_email function tests the change_email_contact function in AddressBook.py
    #         to ensure that it returns an error message when a user attempts to change a contact's email without specifying 
    #         the old email address.
    #     """
    #     contact_name = 'Sasha'
    #     new_email = Email('test_sasha_new@gmail.com')
    #     old_email = None

    #     message = change_email_contact(self.addressbook_test,
    #                                     contact_name,
    #                                     new_email,
    #                                     old_email)
    #     self.assertTrue('After the command, you must enter' in message)

    # def test_delete_email_contact_not_exists_name(self):
    #     """
    #     The test_delete_email_contact_not_exists_name function tests the delete_email_contact function in AddressBook.py
    #         to ensure that it returns a message stating that the contact was not found if a user attempts to delete an email
    #         from a contact who does not exist in their address book.
    #     """
    #     contact_name = 'Sasha'
    #     email = 'test_sasha@gmail.com'

    #     message = delete_email_contact(self.addressbook_test,
    #                                         contact_name,
    #                                         email)
    #     self.assertTrue('was not found' in message)

    # def test_delete_email_contact_not_exists_email(self):
    #     """
    #     The test_delete_email_contact_not_exists_email function tests the delete_email_contact function in the AddressBook module.
    #     The test is designed to check if a contact with an email that does not exist in the address book will return a message stating that it was not found.
    #     """
    #     contact_name = 'Sasha'
    #     email = 'test_sasha_new@gmail.com'

    #     self.addressbook_test.add_record(self.record_test)

    #     message = delete_email_contact(self.addressbook_test,
    #                                         contact_name,
    #                                         email)
    #     self.assertTrue('was not found in the' in message)

    # def test_delete_email_contact_without_name(self):
    #     """
    #     The test_delete_email_contact_without_name function tests the delete_email_contact function in AddressBook.py
    #         to ensure that it returns an error message when a user attempts to delete a contact without specifying the name of 
    #         the contact they wish to delete. The test passes if this is true, and fails otherwise.
    #     """
    #     contact_name = None
    #     email = 'test_sasha@gmail.com'
        
    #     message = delete_email_contact(self.addressbook_test,
    #                                         contact_name,
    #                                         email)
    #     self.assertTrue('After the command, you must enter' in message)

    # def test_delete_email_contact_without_email(self):
    #     """
    #     The test_delete_email_contact_without_email function tests the delete_email_contact function in the AddressBook module.
    #     The test is designed to check if a user can delete an email contact without entering an email address.
    #     If so, then it will return a message saying that after the command, you must enter an email address.
    #     """
    #     contact_name = 'Sasha'
    #     email = None

    #     message = delete_email_contact(self.addressbook_test,
    #                                    contact_name,
    #                                    email)
    #     self.assertTrue('After the command, you must enter' in message)
        
    # def test_print_contacts(self):
    #     """
    #     The function in the AddressBook module.
    #     It does this by creating a mock addressbook, adding a record to it, and then using patch to 
    #     mock sys.stdout so that we can test whether or not the email address of our record is printed out.
    #     """
    #     self.addressbook_test.add_record(self.record_test)
        
    #     with patch('sys.stdout', new=io.StringIO()) as fake_out:
            
    #         print_contacts(self.addressbook_test)
            
    #         self.assertTrue('test_sasha@gmail.com' in fake_out.getvalue())
            
    # def test_print_contact(self):
    #     """
    #     The function in the AddressBook module.
    #     It does this by creating a new addressbook, adding a record to it, and then calling the 
    #     print_contact function on that addressbook with an inputted contact name. It then checks if 
    #     the output of print_contact contains both the user's name and contact's name.
    #     """
    #     contact_name = 'Sasha'
    #     self.addressbook_test.add_record(self.record_test)
        
    #     message = print_contact(self.addressbook_test, contact_name)
        
    #     self.assertTrue(f"{self.user_name}, '{contact_name.title()}':" in message)
        

if __name__ == '__main__':
    unittest.main()