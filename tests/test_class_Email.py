"""Tests class Birthday"""
import unittest
from datetime import date
from entities import Birthday


class TestBirthday(unittest.TestCase):
    """Tests class Birthday"""

    def setUp(self) -> None:
        self.birthday_test = Birthday('26-06-1982')

    def tearDown(self) -> None:
        del self.birthday_test

    def test_birthday_date(self):
        """
        The test_birthday_date function tests the birthday_date attribute of the Birthday class.
        It does this by comparing it to a date object with year 1982, month 6, and day 26.
        """
        
        self.assertEqual(self.birthday_test.birthday_date, date(1982, 6, 26))

    def test_set_birthday(self):
        """
        The test_set_birthday function tests the set_birthday function in the Birthday class.
        It does this by setting a birthday date and then checking if it is equal to a date object.
        """

        self.birthday_test.birthday_date = '15-02-1990'
        self.assertEqual(self.birthday_test.birthday_date, date(1990, 2, 15))

    def test_verify_birthday_date(self):
        """
        The test_verify_birthday_date function tests the verify_birthday_date function in the Birthday class.
        It checks that an error is raised if a date is not entered correctly, and also checks that an error is raised if a future date is entered.
        """
        
        with self.assertRaises(ValueError) as error:
            self.birthday_test.birthday_date = '31-04-2000'
            self.assertTrue('Incorrect date format:' in str(error.exception))

        with self.assertRaises(ValueError)as error:
            self.birthday_test.birthday_date = '30-04-2030'
            self.assertTrue('must be in the past' in str(error.exception))

if __name__ == '__main__':
    unittest.main()