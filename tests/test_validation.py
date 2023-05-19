"""Tests validation"""

import unittest
from validation import (
    name_validation,
    phone_validation,
    birthday_date_validation,
    email_validation,
    criteria_validation,
)


class TestValidation(unittest.TestCase):
    """Tests validation"""

    def test_email_validation_with_invalid_input(self):
        """
        The test_verify_email_with_invalid_input function tests the verify_email function with an invalid input.
        The test is successful if the SystemExit exception is raised and 'Try again!' is printed to stdout.
        """
        email = 'test@sasha@gmail.com'

        with self.assertRaises(ValueError) as context:
            email_validation(email)
        self.assertEqual(str(context.exception), f"Invalid '{email}' email address.")

    def test_verify_email_with_valid_input(self):
        """
        The test_verify_email_with_valid_input function tests the verify_email function with a valid input.
                The expected output is None, and the actual output should be equal to the expected output.
        """
        email = "john.doe@example.com"
        expected_output = None

        actual_output = email_validation(email)

        self.assertEqual(actual_output, expected_output)

    def test_phone_validation_with_invalid_input(self):
        """
        The test_verify_phone_with_invalid_input function tests the verify_phone function in the Phone class.
        It checks that an error is raised if a phone number contains non-digits, or if it's too short or long.
        """
        phone = '+plus380951234567'
        with self.assertRaises(SystemExit) as context:
            phone_validation(phone)
        self.assertEqual('Try again!', context.exception.code)

        phone = '3809'
        with self.assertRaises(SystemExit) as context:
            phone_validation(phone)
        self.assertEqual('Try again!', context.exception.code)

        phone = '380951234567123456789'
        with self.assertRaises(SystemExit) as context:
            phone_validation(phone)
        self.assertEqual('Try again!', context.exception.code)

    def test_name_validation_with_invalid_input(self):
        """
        The test_verify_name function tests the Name class's name property.
        The function raises a TypeError if the new_name variable is not a string, and raises a 
        ValueError if it is an empty string or longer than 50 characters.
        """
        name = 12
        with self.assertRaises(SystemExit) as context:
            name_validation(name)
        self.assertEqual('Try again!', context.exception.code)

        name = 'new_name'
        with self.assertRaises(SystemExit) as context:
            name_validation(name)
        self.assertEqual('Try again!', context.exception.code)

        name = ''
        with self.assertRaises(SystemExit) as context:
            name_validation(name)
        self.assertEqual('Try again!', context.exception.code)

        name = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        with self.assertRaises(SystemExit) as context:
            name_validation(name)
        self.assertEqual('Try again!', context.exception.code)

    def test_birthday_date_validation_with_invalid_input(self):
        """
        The test_verify_birthday_date_with_invalid_input function tests the verify_birthday_date function in the Birthday class.
        It checks that an error is raised if a date is not entered correctly, and also checks that an error is raised if a future date is entered.
        """
        birthday_date = '31-04-2000'
        with self.assertRaises(SystemExit) as context:
            birthday_date_validation(birthday_date)
        self.assertEqual('Try again!', context.exception.code)

        birthday_date = '30-04-2030'
        with self.assertRaises(SystemExit) as context:
            birthday_date_validation(birthday_date)
        self.assertEqual('Try again!', context.exception.code)

    def test_criteria_validation_with_invalid_input(self):
        """
        The test_verify_criteria_with_invalid_input function tests the verify_criteria function with invalid input.
                The test is successful if the SystemExit exception is raised and an error message is printed to stdout.
        """
        criteria = '_'
        with self.assertRaises(SystemExit) as context:
            criteria_validation(criteria)
        self.assertEqual('Try again!', context.exception.code)


if __name__ == '__main__':
    unittest.main()
