"""Tests class User"""
import unittest
from datetime import date

from chat_bot.entities import User


class TestUser(unittest.TestCase):
    """Tests class Name"""

    def setUp(self) -> None:
        self.user_test = User('Sasha')

    def tearDown(self) -> None:
        del self.user_test

    def test_set_name(self):
        """
        The test_set_name function tests the set_name function in the User class.
        It checks that when a user is created, their name is correctly assigned.
        """
        self.assertEqual(self.user_test.name, 'sasha')

   
    def test_set_birthday_date(self):
        """
        The test_set_birthday_date function tests the setter for birthday_date.
        It sets the birthday_date to &quot;01-01-2000&quot; and then checks that it is equal to date(2000, 1, 1)
        """
        self.user_test.birthday_date = "01-01-2000"
        self.assertEqual(self.user_test.birthday_date, date(2000, 1, 1))


if __name__ == '__main__':
    unittest.main()