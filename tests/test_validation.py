"""Tests validation"""

import unittest
from datetime import datetime, timedelta

from my_address_book.entities import User
from my_address_book.address_book import AddressBook as AB, Record
from my_address_book.validation import (
    name_validation,
    phone_validation,
    birthday_date_validation,
    email_validation,
    criteria_validation,
    check_name_in_address_book,
    check_name_not_in_address_book,
)


class TestValidation(unittest.TestCase):
    """Tests validation"""

    def test_email_validation_with_invalid_input(self) -> None:
        """
        The test_verify_email_with_invalid_input function tests the verify_email function with an invalid input.
        The test is successful if the SystemExit exception is raised and 'Try again!' is printed to stdout.
        """
        email = 'test@sasha@gmail.com'

        message_error = email_validation(email)
        self.assertEqual(message_error, "ValueError: Invalid 'test@sasha@gmail.com' email address.")

    def test_email_validation_with_valid_input(self) -> None:
        """
        The test_verify_email_with_valid_input function tests the verify_email function with a valid input.
                The expected output is None, and the actual output should be equal to the expected output.
        """
        email = "john.doe@example.com"

        actual_output = email_validation(email)

        self.assertFalse(actual_output, False)

    def test_phone_validation_with_invalid_input(self) -> None:
        """
        The test_verify_phone_with_invalid_input function tests the verify_phone function in the Phone class.
        It checks that an error is raised if a phone number contains non-digits, or if it's too short or long.
        """
        phone = '+plus380951234567'
        message_error = phone_validation(phone)
        self.assertEqual(
            "TypeError: Contact's phone can only contain digits, but got '+plus380951234567'",
            message_error)

        phone = '3809'
        message_error = phone_validation(phone)
        self.assertEqual(
            "ValueError: Contact's phone must be between 11 and 16 numbers, but got '3809'",
            message_error)

        phone = '380951234567123456789'
        message_error = phone_validation(phone)
        self.assertEqual(
            "ValueError: Contact's phone must be between 11 and 16 numbers, but got '380951234567123456789'",
            message_error)

    def test_phone_validation_with_valid_input(self) -> None:
        """
        The test_phone_validation_with_valid_input function tests the phone_validation function with a valid input.
        The expected output is False, because the phone number is valid.
        """
        phone = "380631234567"

        actual_output = phone_validation(phone)

        self.assertFalse(actual_output, False)

    def test_name_validation_with_invalid_input(self) -> None:
        """
        The test_verify_name function tests the Name class's name property.
        The function raises a TypeError if the new_name variable is not a string, and raises a 
        ValueError if it is an empty string or longer than 50 characters.
        """
        name_invalid_num = 12
        message_error = name_validation(name_invalid_num)
        self.assertEqual("TypeError: Name must be a string, but got int", message_error)

        name_invalid = 'new_name'
        message_error = name_validation(name_invalid)
        self.assertEqual("TypeError: Contact's name can only contain letters, but got 'New_Name'", message_error)

        name_invalid = ''
        message_error = name_validation(name_invalid)
        self.assertEqual("ValueError: Name length must be between 1 and 49, but got ''", message_error)

        name_invalid = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        message_error = name_validation(name_invalid)
        self.assertTrue("ValueError: Name length must be between 1 and 49" in str(message_error))

    def test_name_validation_with_valid_input(self) -> None:
        """
        The test_name_validation_with_valid_input function tests the name_validation function with a valid input.
        The expected output is False, and the actual output is also False.
        """
        name = "Alex"
        actual_output = name_validation(name)
        self.assertFalse(actual_output, False)

    def test_birthday_date_validation_with_invalid_input(self) -> None:
        """
        The test_verify_birthday_date_with_invalid_input function tests the 
        verify_birthday_date function in the Birthday class.
        It checks that an error is raised if a date is not entered correctly, 
        and also checks that an error is raised if a future date is entered.
        """
        birthday_date = datetime.now() + timedelta(days=1)
        message_error = birthday_date_validation(birthday_date.date())
        self.assertEqual(f"ValueError: Birthday '{birthday_date.date()}' must be in the past", message_error)

    def test_criteria_validation_with_invalid_input(self) -> None:
        """
        The test_verify_criteria_with_invalid_input function tests the verify_criteria function with invalid input.
                The test is successful if the SystemExit exception is raised and an error message is printed to stdout.
        """
        criteria = '_'
        message_error = criteria_validation(criteria)
        self.assertEqual("ValueError: Criteria '_' must be only numbers or letters", message_error)

    def test_check_name_in_address_book(self) -> None:
        """
        The test_check_name_in_address_book function checks if the name is already in the address book.
        If it is, then a message will be returned to inform that this contact already exists.
        """
        address_book = AB()
        contact = Record(User("Alex"))
        address_book.add_record(contact)
        name = "Alex"

        message_error = check_name_in_address_book(address_book, name)
        self.assertEqual(f"ValueError: The contact '{name.title()}' already exists in the address book.", message_error)

    def test_check_name_not_in_address_book(self) -> None:
        """
        The test_check_name_not_in_address_book function checks that the name is not in the address book.
            If it is, then an error message will be returned.
        """
        address_book = AB()
        contact = Record(User("Alex"))
        address_book.add_record(contact)
        name = "Olya"

        message_error = check_name_not_in_address_book(address_book, name)
        self.assertEqual(f"KeyError: 'The contact {name.title()} was not found.'", message_error)


if __name__ == '__main__':
    unittest.main()
