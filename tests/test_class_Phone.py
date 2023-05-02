"""Tests class Phone"""
import unittest


from fields import Phone


class TestPhone(unittest.TestCase):
    """Tests class Phone"""

    def setUp(self) -> None:
        self.phone_test = Phone('380951234567')

    def tearDown(self) -> None:
        del self.phone_test

    def test_phone(self):
        """The test_phone function tests the phone number of a person."""

        self.assertEqual(self.phone_test.phone, '+380951234567')

    def test_set_phone(self):
        """
        The test_set_phone function tests the set_phone function of the Phone class.
        It checks if a phone number is correctly formatted and stored in an instance of
        the Phone class.
        """

        self.phone_test.phone = '380989876543'
        self.assertEqual(self.phone_test.phone, '+380989876543')

    def test_eq_phones(self):
        """The test_eq_phones function tests the equality of two phone numbers."""

        phone_test = Phone('380951234567')
        self.assertEqual(phone_test, self.phone_test)

    def test_sanitize_phone_number(self):
        """
        The test_sanitize_phone_number function tests the sanitize_phone_number function in Phone.py
        It takes a phone number as an argument and returns it with all non-numeric characters removed.
        """

        phone_test = self.phone_test.sanitize_phone_number('38(095)123-45-67')
        self.assertEqual(phone_test, '+380951234567')

    def test_verify_phone(self):
        """
        The test_verify_phone function tests the verify_phone function in the Phone class.
        It checks that an error is raised if a phone number contains non-digits, or if it's too short or long.
        """
        with self.assertRaises(TypeError) as error:
            self.phone_test.phone = '+plus380951234567'
        self.assertTrue("Contact's phone can only contain digits, but got" in str(error.exception))

        with self.assertRaises(ValueError) as error:
            self.phone_test.phone = '+3809'
        self.assertTrue("Contact's phone must be between 11 and 16 numbers, but got" in str(error.exception))

        with self.assertRaises(ValueError) as error:
            self.phone_test.phone = '+380951234567123456789'
        self.assertTrue("Contact's phone must be between 11 and 16 numbers, but got" in str(error.exception))


if __name__ == '__main__':
    unittest.main()