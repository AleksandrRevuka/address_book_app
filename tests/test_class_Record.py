"""Test class Record"""
import unittest
from datetime import date, datetime
from fields import Phone
from address_book import Record

class TestRecord(unittest.TestCase):
    """Tests class Record"""

    def setUp(self) -> None:
        self.record_test = Record('Sasha')

    def tearDown(self) -> None:
        del self.record_test

    def test_add_phone_number(self):
        """
        The test_add_phone_number function tests the add_phone_number function of the Record class.
        It creates a phone object and adds it to a record object, then checks if that phone number is in the list of numbers for that record.
        """
        phone = Phone('380951234567')
        self.record_test.add_phone_number(phone)
        self.assertEqual(self.record_test.phone_numbers, [Phone('380951234567')])

    def test_edit_phone_number(self):
        """
        The test_edit_phone_number function tests the edit_phone_number method of the Record class.
        It creates a new record, adds an old phone number to it and then edits this phone number with a new one.
        The test checks if the list of phone numbers in this record contains only one element - our new phone number.
        """
        old_phone = Phone('380951234567')
        new_phone = Phone('380951234500')
        self.record_test.add_phone_number(old_phone)
        self.record_test.edit_phone_number(old_phone, new_phone)
        self.assertEqual(self.record_test.phone_numbers, [new_phone])

    def test_delete_phone_number(self):
        """
        The test_delete_phone_number function tests the delete_phone_number method of the Record class.
        It creates a phone number object and adds it to a record, then deletes it from that record.
        The test passes if the list of phone numbers in that record is empty.
        """
        phone = Phone('380951234567')
        self.record_test.add_phone_number(phone)
        self.record_test.delete_phone_number(phone)
        self.assertEqual(self.record_test.phone_numbers, [])

    def test_add_birthday(self):
        """
        The test_add_birthday function tests the add_birthday function in the Record class.
        It takes a date object as an argument and adds it to the birthday attribute of a record instance.
        """
        self.record_test.add_birthday('26-06-1982')
        self.assertEqual(self.record_test.birthday.birthday_date, date(1982, 6, 26))

    def test_days_to_birthday(self):
        """
        The test_days_to_birthday function tests the days_to_birthday function in Record.py
            It does this by creating a mock date and then comparing it to the birthday of a record object.
            If they are equal, then the test passes.
        """
        current_date = datetime(2023, 1, 1)
    
        self.record_test.add_birthday('1-1-2000')

        # with mock.patch('datetime.datetime') as datetime_mock:
        #     datetime_mock.now.return_value = current_date
            
        self.assertEqual(self.record_test.days_to_birthday(current_date), 0)


if __name__ == '__main__':
    unittest.main()
