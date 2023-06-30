"""Test class Record"""
import unittest
from datetime import datetime

from my_address_book.address_book import RecordContact
from my_address_book.entities import Email
from my_address_book.entities import Phone
from my_address_book.entities import User


class TestRecordContact(unittest.TestCase):
    """Tests class Record"""

    def setUp(self) -> None:
        self.user_test = User("Sasha")
        self.phone_test = Phone("380951234567")
        self.email_test = Email("test_sasha@gmail.com")
        self.record_test = RecordContact(self.user_test)
        self.record_test.add_phone_number(self.phone_test)
        self.record_test.add_email(self.email_test)

    def tearDown(self) -> None:
        del self.record_test
        del self.user_test
        del self.phone_test
        del self.email_test

    def test_add_phone_number(self) -> None:
        """
        The test_add_phone_number function tests the add_phone_number function of the Record class.
        It creates a phone object and adds it to a record object, then checks if that phone number is in the
        list of numbers for that record.
        """

        self.assertEqual(self.record_test.phone_numbers[0].subrecord, Phone("380951234567"))

    def test_add_email(self) -> None:
        """
        The test_add_email function tests the add_email function in Record.py
            The test_add_email function takes a self parameter, which is an instance of the TestRecord class.
            The assertEquals method compares two values and returns True if they are equal, or False otherwise.
        """
        self.assertEqual(self.record_test.emails[0].subrecord, Email("test_sasha@gmail.com"))

    def test_add_birthday(self) -> None:
        """
        The test_add_birthday function tests the add_birthday function in the Record class.
        It takes a date object as an argument and adds it to the birthday attribute of a record instance.
        """
        self.record_test.add_birthday(datetime(1982, 6, 26))
        self.assertEqual(self.record_test.user.birthday_date, datetime(1982, 6, 26))

    def test_days_to_birthday(self) -> None:
        """
        The test_days_to_birthday function tests the days_to_birthday function in Record.py
            It does this by creating a mock date and then comparing it to the birthday of a record object.
            If they are equal, then the test passes.
        """
        current_date = datetime(2023, 1, 1)
        self.record_test.add_birthday(datetime(2000, 1, 1))
        # with mock.patch('datetime.datetime') as datetime_mock:
        #     datetime_mock.now.return_value = current_date
        self.assertEqual(self.record_test.days_to_birthday(current_date), 0)

    def test_days_to_birthday_none(self) -> None:
        """
        The test_days_to_birthday_none function tests the days_to_birthday function in Record.py
            to see if it returns None when the current date is after the birthday of a record.
        """
        current_date = datetime(2023, 1, 1)
        self.assertEqual(self.record_test.days_to_birthday(current_date), None)


if __name__ == "__main__":
    unittest.main()
