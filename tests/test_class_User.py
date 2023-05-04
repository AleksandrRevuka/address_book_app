"""Tests class User"""
import unittest
from datetime import date

from entities import User


class TestUser(unittest.TestCase):
    """Tests class Name"""

    def setUp(self) -> None:
        self.user_test = User('Sasha')
        # self.birthday_test = Birthday('26-06-1982')

    def tearDown(self) -> None:
        del self.user_test

    def test_set_name(self):
        """
        The test_set_name function tests the set_name function in the User class.
        It checks that when a user is created, their name is correctly assigned.
        """
        self.assertEqual(self.user_test.name, 'Sasha')

    def test_verify_name(self):
        """
        The test_verify_name function tests the Name class's name property.
        The function raises a TypeError if the new_name variable is not a string, and raises a 
        ValueError if it is an empty string or longer than 50 characters.
        """
        with self.assertRaises(TypeError) as error:
            self.user_test.name = 12
        self.assertTrue('Name must be a string, but got' in str(error.exception))

        with self.assertRaises(TypeError) as error:
            new_name = 'Sasha1986'
            self.user_test.name = new_name
        self.assertTrue(
            f"Contact's name can only contain letters, but got '{new_name.title()}'", str(error.exception))

        with self.assertRaises(ValueError) as error:
            self.user_test.name = ''
        self.assertTrue('Name length must be between' in str(error.exception))

        with self.assertRaises(ValueError) as error:
            self.user_test.name = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.assertTrue('Name length must be between' in str(error.exception))

    def test_set_birthday_date(self):
        """
        The test_set_birthday_date function tests the setter for birthday_date.
        It sets the birthday_date to &quot;01-01-2000&quot; and then checks that it is equal to date(2000, 1, 1)
        """
        self.user_test.birthday_date = "01-01-2000"
        self.assertEqual(self.user_test.birthday_date, date(2000, 1, 1))

    def test_verify_birthday_date(self):
        """
        The test_verify_birthday_date function tests the verify_birthday_date function in the Birthday class.
        It checks that an error is raised if a date is not entered correctly, and also checks that an error is raised if a future date is entered.
        """
        
        with self.assertRaises(ValueError) as error:
            self.user_test.birthday_date = '31-04-2000'
            self.assertTrue('Incorrect date format:' in str(error.exception))

        with self.assertRaises(ValueError)as error:
            self.user_test.birthday_date = '30-04-2030'
            self.assertTrue('must be in the past' in str(error.exception))

if __name__ == '__main__':
    unittest.main()