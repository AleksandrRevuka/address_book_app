"""Tests class Email"""
import unittest
from datetime import date
from entities import Email


class TestBirthday(unittest.TestCase):
    """Tests class Email"""

    def setUp(self) -> None:
        self.email_test = Email('test_sasha@gmail.com')

    def tearDown(self) -> None:
        del self.email_test

    def test_set_email(self):
        """
        The test_set_email function tests the set_email function in the Email class.
        It checks to see if an email address is properly assigned to a new instance of
        the Email class.
        """
        self.assertEqual(self.email_test.email, 'test_sasha@gmail.com')

    def test_verify_email(self):
        """
        The test_verify_email function tests the email verification function in the Email class.
        It checks to see if an invalid email address is entered, and raises a ValueError exception.
        """
        with self.assertRaises(ValueError) as error:
            self.email_test.email = 'test@sasha@gmail.com'
            self.assertTrue('Invalid email address.' in str(error.exception))

if __name__ == '__main__':
    unittest.main()